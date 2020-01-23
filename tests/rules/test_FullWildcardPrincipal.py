"""
Copyright 2018-2020 Skyscanner Ltd

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import pytest

from cfripper.model.result import Result
from cfripper.rules import FullWildcardPrincipalRule
from tests.utils import get_cfmodel_from


@pytest.fixture()
def good_template():
    return get_cfmodel_from("rules/FullWilcardPrincipalRule/good_template.json").resolve()


@pytest.fixture()
def bad_template():
    return get_cfmodel_from("rules/FullWilcardPrincipalRule/bad_template.json").resolve()


def test_no_failures_are_raised(good_template):
    result = Result()
    rule = FullWildcardPrincipalRule(None, result)
    rule.invoke(good_template)

    assert result.valid
    assert len(result.failed_rules) == 0
    assert len(result.failed_monitored_rules) == 0


def test_failures_are_raised(bad_template):
    result = Result()
    rule = FullWildcardPrincipalRule(None, result)
    rule.invoke(bad_template)

    assert not result.valid
    assert len(result.failed_rules) == 1
    assert len(result.failed_monitored_rules) == 0
    assert result.failed_rules[0].rule == "FullWildcardPrincipalRule"
    assert result.failed_rules[0].reason == "PolicyA should not allow wildcards in principals (principal: '*')"
