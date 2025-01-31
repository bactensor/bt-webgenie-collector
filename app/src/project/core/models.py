from django.db import models
from django.db.models import UniqueConstraint


class Neuron(models.Model):
    hotkey = models.CharField(max_length=48)
    is_active_validator = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["hotkey"], name="unique_%(class)s_hotkey"),
        ]

    def __str__(self) -> str:
        return self.hotkey


class AbstractDataFromValidator(models.Model):
    sender = models.ForeignKey(Neuron, on_delete=models.CASCADE, related_name="%(class)s_data")
    external_id = models.BigIntegerField(help_text="ID as if in Validator's internals")
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        constraints = [
            UniqueConstraint(fields=["sender", "external_id"], name="unique_%(class)s_validator_external_id"),
        ]


class Competition(AbstractDataFromValidator):
    name = models.CharField()

    def __str__(self) -> str:
        return self.name


class LeaderboardSession(AbstractDataFromValidator):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="leaderboard_sessions")
    created_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self) -> str:
        return f"Session {self.pk}"


class Challenge(AbstractDataFromValidator):
    session = models.ForeignKey(LeaderboardSession, on_delete=models.CASCADE, related_name="challenges")
    ground_truth_html = models.TextField()

    def __str__(self) -> str:
        return f"Challenge {self.pk}"


class TaskSolution(AbstractDataFromValidator):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="task_solutions")
    created_at = models.DateTimeField()
    miner_answer = models.JSONField()

    def __str__(self) -> str:
        return f"Solution {self.pk}"


class EvaluationType(AbstractDataFromValidator):
    name = models.CharField()

    def __str__(self) -> str:
        return self.name


class Judgement(AbstractDataFromValidator):
    miner = models.ForeignKey(Neuron, on_delete=models.CASCADE, related_name="miner_judgements")
    validator = models.ForeignKey(Neuron, on_delete=models.CASCADE, related_name="validator_judgements")

    def __str__(self) -> str:
        return f"Judgement {self.pk}"


class SolutionEvaluation(AbstractDataFromValidator):
    judgement = models.ForeignKey(Judgement, on_delete=models.CASCADE, related_name="solution_evaluations")
    evaluation_type = models.ForeignKey(EvaluationType, on_delete=models.CASCADE, related_name="solution_evaluations")
    task_solution = models.ForeignKey(TaskSolution, on_delete=models.CASCADE, related_name="solution_evaluations")
    value = models.FloatField()

    def __str__(self) -> str:
        return f"Evaluation {self.pk}: {self.value}"
