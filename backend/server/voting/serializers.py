from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.utils import timezone

from .models import Poll, PollOption, PollVote
from backend.server.voting.serializers import PollSerializer
from backend.server.society.serializers import validate


class PollOptionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = PollOption
        fields = ['id', 'poll', 'text', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class PollSerializer(serializers.ModelSerializer):
    option = PollOptionSerializer(many=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), required=False)
    class Meta:
        model = Poll
        fiels =  (
            "id",
            "title",
            "description",
            "created_by",
            "start_date",
            "end_date",
            "max_votes",
            "is_active",
            "options",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

        def validate(self, attrs):
            #For Partial Updates we take the new values or exiting value if not provided and check for validation
            start = attrs.get("start_date", getattr(self.instance, "start_date", None))
            end = attrs.get("end_date", getattr(self.instance, "end_date", None))
            if start and end and start >= end:
                raise serializers.ValidationError("Start date must be before end date.")
            return attrs
        #strip() -> Trimming a function in python for removing unwanted whitespaces
        def validate_options(self, value): 
            text = [option.get("text", "").strip() for option in value]
            if "" in text: 
                raise serializers.ValidationError("Option text cannot be empty")
            return value

        def _set_created_by_default(self, validated_data):
            if 'created_by' not in validated_data:
                req = self.context.get('request')
                if req and getattr(req, 'user') and req.user.is_authenticated:
                    validated_data['created_by'] = req.user
                else:
                    raise serializers.ValidationError("Created by field is required.")

        #bulk_create() -> A method in Django ORM to create multiple objects at once
        def create(self, validated_data):
            options_data = validated_data.pop("options", [])
            self._set_created_by_default(validated_data)
            with transaction.atomic():
                poll = Poll.objects.create(**validated_data)
                if options_data:
                    PollOption.objects.bulk_create(
                        [PollOption(poll=poll, text=option["text"]) for option in options_data]
                    )
            return poll

        #update() -> A method in Django ORM to update an existing object
        #instance -> An existing object that is being updated
        #validated_data -> The new data that is being used to update the object
        #setattr() -> A built-in Python function to set an attribute dynamically on an object
        def update(self, instance, validated_data):
            options_data = validated_data.pop("options", None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            with transaction.atomic():
                instance.save()

                if options_data is not None:
                    # Get all existing options of the poll from the database
                    existing = {option.id: option for option in instance.options.all()}
                    seen_ids = set ()
                    to_create =  []

                    for option in options_data:
                        option_id = option.get("id")
                        updated_text = option.get("text", "").strip()
                        if not updated_text:
                            raise serializers.ValidationError({"option": "Option text is required."})
                        if option_id and option_id in existing:
                            obj = existing[option_id]
                            obj.text = updated_text
                            obj.save(update_fields=['text', 'updated_at'])
                            seen_ids.add(option_id)
                        else:
                            to_create.append(PollOption(poll=instance, text=updated_text))
                    # Insert new options
                    if to_create:
                        PollOption.objects.bulk_create(to_create)
                    # Delete options that were not in the update if this is a PUT request
                    request = self.context.get('request')
                    is_put = request and request.method == 'PUT'
                    if is_put:
                        for option_id in existing:
                            if option_id not in seen_ids:
                                existing[option_id].delete()
            return instance

class PollVoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(), required=False
    )

    class Meta:
        model = PollVote
        fields = ("id", "user", "poll", "option", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):

        req = self.context.get('request')
        user = attrs.get('user')
        if req and getattr(req, 'user', None) and req.user.is_authenticated:
            if not user:
                attrs['user'] = req.user
            elif not user or user != req.user:
                raise serializers.ValidationError("User must be authenticated to vote.")

            option = attrs.get('option')
            poll = attrs.get('poll') or (option.poll if option else None)

            if not poll or not option:
                 raise serializers.ValidationError("Both poll and option are required.")
            
            if option.poll_id != poll.id:
                raise serializers.ValidationError(
                {"option": "Option does not belong to the specified poll."}
            )

            now = timezone.now()
            if not poll.is_active or not (poll.start_date <= now <= poll.end_date):
                raise serializers.ValidationError("Poll is not active or is outside the voting period.")
            
            existing_count = PollVote.objects.filter(
                poll=poll, user=attrs["user"]
            ).count()

            if existing_count >= poll.max_votes:
                raise serializers.ValidationError(
                    f"User has already voted {existing_count} times, exceeding the maximum of {poll.max_votes} votes."
                )
            
            attrs['poll'] = poll
            return attrs
      
    def create(self, validate_data):
        try:
            with transaction.atomic():
                return super().create(validate_data)
        except IntegrityError:
            raise serializers.ValidationError("Vote creation failed due to integrity error.")
