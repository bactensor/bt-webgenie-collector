import json
import time
from io import BufferedReader

import pytest
import requests
from bittensor import Wallet

TEST_PAYLOAD = {
    "external_id": 1,
    "name": "Competition 1",
    "leaderboard_sessions": [
        {
            "external_id": 3,
            "created_at": "2025-01-18T06:00:00Z",
            "challenges": [
                {
                    "external_id": 5,
                    "ground_truth_html": "Groundtruth HTML for challenge 1",
                    "task_solutions": [
                        {
                            "external_id": 5,
                            "created_at": "2025-01-18T09:38:59Z",
                            "miner_answer": {"this is": "miner answer"},
                            "solution_evaluations": [
                                {
                                    "external_id": 6,
                                    "judgement": {"external_id": 6, "miner": "neuron-two", "validator": "neuron-three"},
                                    "evaluation_type": {"external_id": 6, "name": "Pagespeed rank"},
                                    "value": 0.93,
                                }
                            ],
                        }
                    ],
                },
                {"external_id": 6, "ground_truth_html": "Groundtruth HTML for challenge 2", "task_solutions": []},
            ],
        }
    ],
}


def make_signed_request(
    wallet: Wallet,
    url: str,
    subnet_id: int,
    payload: dict,
    method: str = "POST",
    file_path: str | None = None,
    subnet_chain: str = "mainnet",
) -> requests.Response:
    headers = {
        "Realm": subnet_chain,
        "SubnetID": str(subnet_id),
        "Nonce": str(time.time()),
        "Hotkey": wallet.hotkey.ss58_address,
    }

    file_content = b""
    files = None
    if file_path:
        # TODO: start context for opening file
        opened_file = open(file_path, "rb")
        files = {"file": opened_file}
        file = files.get("file")

        if isinstance(file, BufferedReader):
            file_content = file.read()
            file.seek(0)

    headers_str = json.dumps(headers, sort_keys=True)
    data_to_sign = f"{method}{url}{headers_str}{file_content.decode(errors='ignore')}".encode()
    signature = wallet.hotkey.sign(
        data_to_sign,
    ).hex()
    headers["Signature"] = signature

    response = requests.request(method, url, headers=headers, files=files, json=payload, timeout=5)
    return response


@pytest.mark.skip
def test_send_payload() -> None:
    wallet = Wallet()

    response = make_signed_request(
        wallet=wallet,
        url="http://127.0.0.1:8000/api/competitions/",
        subnet_id=12,
        method="POST",
        payload=TEST_PAYLOAD,
    )
    if not response.ok:
        print(response.json())


if __name__ == "__main__":
    test_send_payload()
