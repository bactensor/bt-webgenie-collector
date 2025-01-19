import bittensor
from bittensor import NeuronInfo
import structlog
from celery import Task
from celery.utils.log import get_task_logger
from django.conf import settings

from .models import Neuron

from ..celery import app

logger = structlog.wrap_logger(get_task_logger(__name__))


def is_validator(neuron: NeuronInfo) -> bool:
    return neuron.stake > 1_000


def send_to_dead_letter_queue(task: Task, exc, task_id, args, kwargs, einfo):
    """Hook to put a task into dead letter queue when it fails."""
    if task.app.conf.task_always_eager:
        return  # do not run failed task again in eager mode

    logger.warning(
        "Sending failed task to dead letter queue",
        task=task,
        exc=exc,
        task_id=task_id,
        args=args,
        kwargs=kwargs,
        einfo=einfo,
    )
    task.apply_async(args=args, kwargs=kwargs, queue="dead_letter")


@app.task()
def sync_validators() -> None:
    metagraph = bittensor.metagraph(netuid=settings.BITTENSOR_NETUID, network=settings.BITTENSOR_NETWORK)
    active_validators_keys = [neuron.hotkey for neuron in metagraph.neurons if is_validator(neuron)]

    to_deactivate = Neuron.objects.filter(is_active_validator=True).exclude(hotkey__in=active_validators_keys)
    num_deactivated = to_deactivate.update(is_active_validator=False)
    logger.debug("validators deactivated", num_deactivated=num_deactivated)

    to_activate = Neuron.objects.filter(is_active_validator=False, hotkey__in=active_validators_keys)
    num_activated = to_activate.update(is_active_validator=True)
    logger.debug("validators activated", num_activated=num_activated)

    to_create = set(active_validators_keys) - set(Neuron.objects.filter(is_active_validator=True).values_list("hotkey", flat=True))
    num_created = Neuron.objects.bulk_create(
        [Neuron(hotkey=hotkey, is_active_validator=True) for hotkey in to_create]
    )
    logger.debug("validators created", num_created=num_created)
