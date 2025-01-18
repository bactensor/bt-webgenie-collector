from django.db import transaction
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import (
    Challenge,
    Competition,
    EvaluationType,
    Judgement,
    LeaderboardSession,
    Neuron,
    SolutionEvaluation,
    TaskSolution,
)


class BaseSerializer(ModelSerializer):

    class Meta:
        fields = "external_id",

    def create(self, validated_data: dict) -> object:
        assert 'sender' in validated_data, f"sender not in {validated_data}"

        model = self.Meta.model
        with transaction.atomic():
            try:
                return model.objects.get(sender=validated_data['sender'], external_id=validated_data['external_id'])
            except model.DoesNotExist:
                return super().create(validated_data)

    def update(self, instance: object, validated_data: dict) -> object:
        raise NotImplementedError(f'Update not implemented for {instance.__class__.__name__}')


class EvaluationTypeSerializer(BaseSerializer):

    class Meta:
        model = EvaluationType
        fields = (
            *BaseSerializer.Meta.fields,
            "name",
        )


class NeuronSerializer(ModelSerializer):

    class Meta:
        model = Neuron
        fields = (
            "hotkey",
        )


class JudgementSerializer(BaseSerializer):
    miner = SlugRelatedField(slug_field="hotkey", queryset=Neuron.objects.all())
    validator = SlugRelatedField(slug_field="hotkey", queryset=Neuron.objects.all())

    class Meta(BaseSerializer.Meta):
        model = Judgement
        fields = (
            *BaseSerializer.Meta.fields,
            "miner",
            "validator",
        )

    def create(self, validated_data: dict) -> Judgement:
        miner, _ = Neuron.objects.get_or_create(hotkey=validated_data.pop("miner"))
        validator, _ = Neuron.objects.get_or_create(hotkey=validated_data.pop("validator"))
        return super().create({
            **validated_data,
            'miner': miner,
            'validator': validator,
        })


class SolutionEvaluationSerializer(BaseSerializer):
    judgement = JudgementSerializer()
    evaluation_type = EvaluationTypeSerializer()

    class Meta(BaseSerializer.Meta):
        model = SolutionEvaluation
        fields = (
            *BaseSerializer.Meta.fields,
            "judgement",
            "evaluation_type",
            "value",
        )

    def create(self, validated_data: dict) -> SolutionEvaluation:
        judgement = JudgementSerializer().create(validated_data.pop("judgement") | {"sender": validated_data['sender']})
        evaluation_type = EvaluationTypeSerializer().create(validated_data.pop("evaluation_type") | {"sender": validated_data['sender']})
        return super().create({
            **validated_data,
            'judgement': judgement,
            'evaluation_type': evaluation_type,
        })

class TaskSolutionSerializer(BaseSerializer):
    solution_evaluations = SolutionEvaluationSerializer(many=True)

    class Meta(BaseSerializer.Meta):
        model = TaskSolution
        fields = (
            *BaseSerializer.Meta.fields,
            "created_at",
            "miner_answer",
            "solution_evaluations",
        )

    def create(self, validated_data: dict) -> TaskSolution:
        solution_evaluations = validated_data.pop('solution_evaluations')

        task_solution = super().create(validated_data)
        for solution_evaluation in solution_evaluations:
            SolutionEvaluationSerializer().create({
                **solution_evaluation,
                "sender": validated_data['sender'],
                "task_solution": task_solution,
            })

        return task_solution


class ChallengeSerializer(BaseSerializer):
    task_solutions = TaskSolutionSerializer(many=True)

    class Meta(BaseSerializer.Meta):
        model = Challenge
        fields = (
            *BaseSerializer.Meta.fields,
            "ground_truth_html",
            "task_solutions",
        )

    def create(self, validated_data: dict) -> Challenge:
        task_solutions = validated_data.pop('task_solutions')

        challenge = super().create(validated_data)
        for task_solution in task_solutions:
            TaskSolutionSerializer().create({
                **task_solution,
                "sender": validated_data['sender'],
                "challenge": challenge,
            })

        return challenge

class LeaderboardSessionSerializer(BaseSerializer):
    challenges = ChallengeSerializer(many=True)

    class Meta(BaseSerializer.Meta):
        model = LeaderboardSession
        fields = (
            *BaseSerializer.Meta.fields,
            "created_at",
            "challenges",
        )

    def create(self, validated_data: dict) -> LeaderboardSession:
        challenges = validated_data.pop('challenges')

        leaderboard_session = super().create(validated_data)
        for challenge in challenges:
            ChallengeSerializer().create({
                **challenge,
                "sender": validated_data['sender'],
                "session": leaderboard_session,
            })

        return leaderboard_session


class CompetitionSerializer(BaseSerializer):
    sender = NeuronSerializer(read_only=True)
    leaderboard_sessions = LeaderboardSessionSerializer(many=True)

    class Meta(BaseSerializer.Meta):
        model = Competition
        fields = (
            "sender",
            *BaseSerializer.Meta.fields,
            "name",
            "leaderboard_sessions",
        )

    def create(self, validated_data: dict) -> Competition:
        sender_hotkey = self.context['request'].headers['Hotkey']
        sender, _ = Neuron.objects.get_or_create(hotkey=sender_hotkey)

        leaderboard_sessions = validated_data.pop('leaderboard_sessions')

        competition = super().create(validated_data | {"sender": sender})
        for leaderboard_session in leaderboard_sessions:
            LeaderboardSessionSerializer().create({
                **leaderboard_session,
                "sender": sender,
                "competition": competition,
            })

        return competition
