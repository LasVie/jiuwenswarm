# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Structured OpenCLI execution guarded by progressive Skill disclosure."""

from jiuwenswarm.agents.harness.common.opencli.contracts import (
    OPENCLI_WEB_SKILL_NAME,
)
from jiuwenswarm.agents.harness.common.opencli.disclosure import (
    DisclosureReceiptStore,
    get_opencli_disclosure_store,
)
from jiuwenswarm.agents.harness.common.opencli.rail import (
    OpenCLIDisclosureRail,
)
from jiuwenswarm.agents.harness.common.opencli.tool import (
    OPENCLI_EXECUTE_TOOL_NAME,
    OpenCLIExecuteTool,
)

__all__ = [
    "DisclosureReceiptStore",
    "OPENCLI_EXECUTE_TOOL_NAME",
    "OPENCLI_WEB_SKILL_NAME",
    "OpenCLIDisclosureRail",
    "OpenCLIExecuteTool",
    "get_opencli_disclosure_store",
]
