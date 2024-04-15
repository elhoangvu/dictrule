r"""
       ___      __             __   
  ____/ (_)____/ /________  __/ /__ 
 / __  / / ___/ __/ ___/ / / / / _ \
/ /_/ / / /__/ /_/ /  / /_/ / /  __/
\__,_/_/\___/\__/_/   \__,_/_/\___/ 

"""

from typing import (
    Any,
    List,
    Dict,
    Set,
    Union,
    Optional,
)

from .built_in_rules import (
    BlockRule,
    CommentRule,
    EvalRule,
    InlineRule,
    IndentRule,
    ForInRule,
    JoinBlockRule,
    JoinEvalRule,
    FormatRule,
    StringifyRule,
)

from .rule import Rule
from .context import Context
from .exceptions import (
    InvalidTypeException,
    NoneValueException,
)


class Generator:
    """Manage rules and a generator for rules by dictionary"""

    STD_RULES = [
        BlockRule(),
        CommentRule(),
        EvalRule(),
        InlineRule(),
        IndentRule(),
        ForInRule(),
        JoinBlockRule(),
        JoinEvalRule(),
        FormatRule(),
        StringifyRule(),
    ]

    def __init__(
        self,
        gen_rules: List[Union[str, Dict[str, Any]]],
        parse_rules: Optional[List[Rule]] = None,
    ):
        """Initialization method for DictRule.

        Args:
            gen_rules (List[Union[str, Dict[str, Any]]]): List or dictionary of rules
            parse_rules (Optional[List[Rule]], optional):
                List of rule parsers bases on `Rule`.
                Defaults to `DictRule.STD_RULES`.
        """
        if parse_rules is None:
            parse_rules = Generator.STD_RULES

        self._cache_rules: Dict[str, Rule] = {}
        self._gen_rules = list(gen_rules)
        self._parse_rules: List[Rule] = []
        self.add_parse_rules(parse_rules)

    @property
    def parse_rules(self) -> List[Rule]:
        """Getter for `parse_rules` property"""

        return self._parse_rules

    @property
    def gen_rules(self) -> List[Union[str, Dict[str, Any]]]:
        """Getter for `gen_rules` property"""

        return self._gen_rules

    def add_parse_rule(
        self,
        rule: Rule,
    ):
        """Adds an extra rule to the parser.

        Args:
            rule (Rule): The rule subclass to add.
        """

        self._parse_rules.append(rule)

    def add_parse_rules(
        self,
        rules: List[Rule],
    ):
        """Adds a list of extra rules to parser.

        Args:
            rules (List[Rule]): List of rules, each being a subclass of Rule.
        """
        for rule in rules:
            self.add_parse_rule(rule)

    def generate(
        self,
        context: Optional[Context] = None,
    ) -> str:
        """Generate text based on `gen_rules`, `parse_rules` and `context`

        Args:
            context (Optional[Context], optional): The context to parse the rule.
                Defaults to None.
                @see `dicturle.Context`

        Returns:
            str: Generated text
        """

        def _rule_from_dict(rule_dict: Dict[str, Any]) -> Rule:
            rule = self._parse_rule_from_dict(rule_dict)
            if not rule:
                pass

            if rule is None:
                raise NoneValueException(f"Not found any rule in dict {rule_dict}")

            return rule

        def _internal_parse_rule(
            context: Optional[Context],
            rule: Any,
        ) -> str:
            if not rule:
                return ""

            if isinstance(rule, str):
                return rule

            if not isinstance(rule, Dict):
                raise InvalidTypeException(f"Rule {rule} must be a dict")

            found_rule = _rule_from_dict(rule)
            parsed = found_rule.parse(
                rule_dict=rule,
                context=context,
                rule_callback=_internal_parse_rule,
            )

            return parsed

        self._parse_rules.sort(
            key=lambda r: len(r.dr_non_optional_props),
            reverse=True,
        )

        output: List[str] = []
        for rule in self._gen_rules:
            parsed = _internal_parse_rule(
                context=context,
                rule=rule,
            )
            output.append(parsed)

        return "\n".join(output)

    def _parse_rule_from_dict(
        self,
        rule_dict: Dict[str, Any],
    ) -> Optional[Rule]:
        dict_keys = set(rule_dict.keys())
        key = self._key_from_keys(dict_keys)
        rule = self._cache_rules.get(key)
        if rule:
            return rule

        for rule in self._parse_rules:
            props: Set[str] = set()
            for prop in rule.dr_non_optional_props:
                prop_name, prop_value = prop(rule_dict)
                if not prop_value:
                    props = set()
                    break

                props.add(prop_name)

            if len(props) == 0:
                continue

            return rule

        return None

    def _key_from_keys(
        self,
        keys: Set[str],
    ) -> str:
        return ".".join(sorted(keys))
