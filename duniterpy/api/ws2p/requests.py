import json
import re
from typing import Optional

from duniterpy.helpers import get_ws2p_challenge
from duniterpy.api.bma.blockchain import BLOCK_SCHEMA, BLOCKS_SCHEMA

ERROR_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "resId": {
            "type": "string",
            "pattern": "^[0-9,a-z,A-Z]{8}$"
        },
        "err": {"type": "string"}
    },
    "required": ["resId", "err"]
}

BLOCK_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "resId": {
            "type": "string",
            "pattern": "^[0-9,a-z,A-Z]{8}$"
        },
        "body": BLOCK_SCHEMA
    },
    "required": ["resId", "body"]
}

BLOCKS_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "resId": {
            "type": "string",
            "pattern": "^[0-9,a-z,A-Z]{8}$"
        },
        "body": BLOCKS_SCHEMA
    },
    "required": ["resId", "body"]
}

REQUIREMENTS_SCHEMA = {
    "type": "object",
    "properties": {
        "identities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "certifications": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "from": {
                                    "type": "string"
                                },
                                "to": {
                                    "type": "string"
                                },
                                "expiresIn": {
                                    "type": "number"
                                },
                                "timestamp": {
                                    "type": "number"
                                }
                            },
                            "required": ["from", "to", "expiresIn", "timestamp"]
                        }
                    },
                    "expired": {
                        "type": "boolean"
                    },
                    "isSentry": {
                        "type": "boolean"
                    },
                    "membershipExpiresIn": {
                        "type": "number"
                    },
                    "membershipPendingExpiresIn": {
                        "type": "number"
                    },
                    "meta": {
                        "type": "object",
                        "properties": {
                            "timestamp": {
                                "type": "string"
                            }
                        },
                        "required": ["timestamp"]
                    },
                    "outdistanced": {
                        "type": "boolean"
                    },
                    "pendingCerts": {
                        "type": "array",
                        "items" : {
                            "type": "object",
                            "properties": {
                                "block": {"type": "number"},
                                "block_hash": {"type": "string"},
                                "block_number": {"type": "number"},
                                "blockstamp": {"type": "string"},
                                "expired": {"type": "number", "const": 0},
                                "expires_on": {"type": "number"},
                                "from": {"type": "string"},
                                "linked": {"type": "boolean", "const": False},
                                "sig": {"type": "string"},
                                "target": {"type": "string"},
                                "to": {"type": "string"},
                                "written": {"type": "boolean", "const": False},
                                "written_block": {"type": ["string", "null"], "const": None},
                                "written_hash": {"type": ["string", "null"], "const": None}
                            }
                        }
                    },
                    "pendingMemberships": {
                        "type": "array",
                        "items" : {
                            "type": "object",
                            "properties": {
                                "block": {"type": "string"},
                                "blockHash": {"type": "string"},
                                "blockNumber": {"type": "number"},
                                "blockstamp": {"type": "string"},
                                "certts": {"type": "string"},
                                "expired": {"type": ["number", "null"], "const": None},
                                "expires_on": {"type": "number"},
                                "fpr": {"type": "string"},
                                "idtyHash": {"type": "string"},
                                "issuer": {"type": "string"},
                                "membership": {"type": "string", "enum": ["IN", "OUT"]},
                                "number": {"type": "number"},
                                "sig": {"type": "string"},
                                "signature": {"type": "string"},
                                "type": {"type": "string"},
                                "userid": {"type": "string"},
                                "linked": {"type": "boolean", "const": False},
                                "written_number": {"type": ["number", "null"], "const": None},
                            }
                        }
                    },
                    "pubkey": {
                        "type": "string"
                    },
                    "revokation_sig": {
                        "type": ["string", "null"]
                    },
                    "revoked": {
                        "type": "boolean"
                    },
                    "sig": {
                        "type": "string"
                    },
                    "uid": {
                        "type": "string"
                    },
                    "wasMember": {
                        "type": "boolean"
                    },
                },
                "required": ["certifications", "expired", "isSentry", "membershipExpiresIn",
                             "membershipPendingExpiresIn", "meta", "outdistanced", "pendingCerts",
                             "pendingMemberships", "pubkey", "revocation_sig", "revoked", "sig", "uid", "wasMember"]
            }
        }
    },
    "required": ["identities"]
}

REQUIREMENTS_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "resId": {
            "type": "string",
            "pattern": "^[0-9,a-z,A-Z]{8}$"
        },
        "body": REQUIREMENTS_SCHEMA
    },
    "required": ["resId", "body"]
}


def get_current(request_id: Optional[str] = None) -> str:
    """
    Return ws2p getCurrent() request as json string

    :return:
    """
    if request_id is None:
        request_id = get_ws2p_challenge()[:8]
    else:
        if not re.fullmatch("^[0-9a-zA-Z]{8}$", request_id):
            raise Exception("Invalid ws2p request unique id")
    return json.dumps({
        "reqId": request_id,
        "body": {
            "name": "CURRENT",
            "params": {}
        }
    })


def get_block(block_number: int, request_id: Optional[str] = None) -> str:
    """
    Return ws2p getBlock() request as json string

    :return:
    """
    if request_id is None:
        request_id = get_ws2p_challenge()[:8]
    else:
        if not re.fullmatch("^[0-9a-zA-Z]{8}$", request_id):
            raise Exception("Invalid ws2p request unique id")
    return json.dumps({
        "reqId": request_id,
        "body": {
            "name": "BLOCK_BY_NUMBER",
            "params": {
                "number": block_number
            }
        }
    })


def get_blocks(from_number: int, count: int, request_id: Optional[str] = None) -> str:
    """
    Return ws2p getBlocks(fromNumber, count) request as json string

    :return:
    """
    if request_id is None:
        request_id = get_ws2p_challenge()[:8]
    else:
        if not re.fullmatch("^[0-9a-zA-Z]{8}$", request_id):
            raise Exception("Invalid ws2p request unique id")
    return json.dumps({
        "reqId": request_id,
        "body": {
            "name": "BLOCKS_CHUNK",
            "params": {
                "fromNumber": from_number,
                "count": count
            }
        }
    })


def get_requirements_pending(min_cert: int, request_id: Optional[str] = None) -> str:
    """
    Return ws2p getRequirementsPending(minCert) request as json string

    :return:
    """
    if request_id is None:
        request_id = get_ws2p_challenge()[:8]
    else:
        if not re.fullmatch("^[0-9a-zA-Z]{8}$", request_id):
            raise Exception("Invalid ws2p request unique id")
    return json.dumps({
        "reqId": request_id,
        "body": {
            "name": "WOT_REQUIREMENTS_OF_PENDING",
            "params": {
                "minCert": min_cert
            }
        }
    })