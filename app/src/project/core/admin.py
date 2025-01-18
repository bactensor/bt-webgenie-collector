from django.contrib import admin
from django.contrib.admin import register
from django.db.models import QuerySet
from django.http import HttpRequest
from .models import (
    Neuron,
    Competition,
    LeaderboardSession,
    Challenge,
    TaskSolution,
    EvaluationType,
    Judgement,
    SolutionEvaluation,
)


admin.site.site_header = "project Administration"
admin.site.site_title = "project"
admin.site.index_title = "Welcome to project Administration"


@register(Neuron)
class NeuronAdmin(admin.ModelAdmin):
    list_display = "pk", "hotkey", "is_active_validator",
    list_filter = "is_active_validator",
    search_fields = "hotkey",
    ordering = "hotkey",


@register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = "pk", "external_id", "name", "received_at",
    list_filter = "received_at",
    search_fields = "name",
    autocomplete_fields = "sender",
    ordering = "-pk",


@register(LeaderboardSession)
class LeaderboardSessionAdmin(admin.ModelAdmin):
    list_display = "pk", "external_id", "competition", "created_at", "received_at",
    list_filter = "received_at", "created_at",
    search_fields = "competition__name",
    autocomplete_fields = "sender", "competition",
    ordering = "-pk",

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("competition")


@register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = "pk", "external_id", "session", "ground_truth_html", "received_at",
    list_filter = "received_at", "session",
    search_fields = "session__competition__name",
    autocomplete_fields = "sender", "session",
    ordering = "-pk",

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("session__competition")


@register(TaskSolution)
class TaskSolutionAdmin(admin.ModelAdmin):
    list_display = "pk", "external_id", "challenge", "created_at", "miner_answer", "received_at",
    list_filter = "received_at", "challenge",
    search_fields = "challenge__session__competition__name",
    autocomplete_fields = "sender", "challenge",
    ordering = "-pk",

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("challenge__session__competition")


@register(EvaluationType)
class EvaluationTypeAdmin(admin.ModelAdmin):
    list_display = "pk", "external_id", "name", "received_at",
    list_filter = "received_at",
    search_fields = "name",
    autocomplete_fields = "sender",
    ordering = "name",


@register(Judgement)
class JudgementAdmin(admin.ModelAdmin):
    list_display = "pk", "external_id", "sender", "miner", "validator", "received_at",
    list_filter = "received_at",
    search_fields = "sender__hotkey", "miner__hotkey", "validator__hotkey",
    autocomplete_fields = "sender", "miner", "validator",
    ordering = "-pk",

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("sender", "miner", "validator")


@register(SolutionEvaluation)
class SolutionEvaluationAdmin(admin.ModelAdmin):
    list_display = "pk", "external_id", "judgement", "evaluation_type", "value", "received_at",
    list_filter = "received_at", "evaluation_type",
    search_fields = "judgement__sender__hotkey", "judgement__miner__hotkey", "judgement__validator__hotkey",
    autocomplete_fields = "sender", "judgement", "evaluation_type", "task_solution",
    ordering = "-pk",

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related("judgement__sender", "judgement__miner", "judgement__validator", "evaluation_type")
