"""Comment rule module"""

from typing import (
    Dict,
    Any,
    Optional,
    Callable,
)

from enum import Enum
from ..dr_property import dr_property
from ..rule import Rule
from ..context import Context
from ..exceptions import (
    NoneValueException,
    InvalidTypeException,
    InvalidValueException,
)


class CommentRule(Rule):
    """This rule allows generating comment text based on single-line and multi-line rules.

    Building `Context` with `CommentRule.ContextCase` to define the comment style.

    Examples:
    ---------
    >>> context = build_singleline_context("#")
    >>> dictrule.Generator({
    ...     "comment": "This is a single-line comment"
    ... }).generate(context)
    # This is a single-line comment

    >>> context = build_multiline_context('\"""')
    >>> dictrule.Generator({
    ...     "style": "multiline",
    ...     "comment": [
    ...         "line1": "Line 1 of multi-line comment",
    ...         "line2": "Line 2 of multi-line comment",
    ...     ]
    ... }).generate(context)
    \"""
    Line 1 of multi-line comment
    Line 2 of multi-line comment
    \"""
    """

    CONTEXT_NAME = "comment"

    @dr_property()
    def _comment(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `comment` attribute."""

    @dr_property(optional=True)
    def _style(self, props: Dict[str, Any]) -> Any:
        """Property method for retrieving the `style` attribute."""

    class ContextCase(Context.Case):
        """`Context.Case` for `CommentRule`.

        This class defines different contexts for the CommentRule,
            including configurations for single-line and multi-line comments.

        Attributes:
            name (str): The name of the context, inherited from Context.Case.
            singleline (Optional[SinglelineComment]): Configuration for single-line comments.
            multiline (Optional[MultilineComment]): Configuration for multi-line comments.
        """

        class Comment:
            """Abstract class for `Commentrule.Comment`"""

            @staticmethod
            @property
            def style() -> "CommentRule.Style":
                """Comment style"""

                return None

        class SinglelineComment(Comment):
            """Singleline comment by prefix"""

            def __init__(
                self,
                prefix: str,
            ):
                """Initial method for `SinglelineComment`

                Args:
                    prefix (str): prefix for each line
                """

                self._prefix = prefix

            @staticmethod
            @property
            def style() -> "CommentRule.Style":
                return CommentRule.Style.SINGLELINE

            @property
            def prefix(self) -> str:
                """Getter for `prefix` property"""

                return self._prefix

        class MultilineComment(Comment):
            """Multiline comment by comment open, comment close, and prefix for each line"""

            def __init__(
                self,
                open_comment: str,
                close_comment: str,
                prefix: str,
            ):
                """Initial method for `MultilineComment`

                Args:
                    open_comment (str): open text of comment
                    close_comment (str): close text of comment
                    prefix (str): prefix for each line
                """

                self._prefix = prefix
                self._open_comment = open_comment
                self._close_comment = close_comment

            @staticmethod
            @property
            def style() -> "CommentRule.Style":
                return CommentRule.Style.MULTILINE

            @property
            def prefix(self) -> str:
                """Getter for `prefix` property"""

                return self._prefix

            @property
            def open_comment(self) -> str:
                """Getter for `open_comment` property"""

                return self._open_comment

            @property
            def close_comment(self) -> str:
                """Getter for `close_comment` property"""

                return self._close_comment

        @property
        def name(self) -> str:
            """Getter for `name` property"""

            return CommentRule.CONTEXT_NAME

        def __init__(
            self,
            singleline: Optional[SinglelineComment] = None,
            multiline: Optional[MultilineComment] = None,
        ):
            """Inital method for `ContextCase`

            Args:
                singleline (Optional[SinglelineComment], optional): singleline config.
                    Defaults to None.
                multiline (Optional[MultilineComment], optional): multiline config.
                    Defaults to None.
            """

            self._singleline = singleline
            self._multiline = multiline

        @property
        def singleline(self) -> SinglelineComment:
            """Getter for `singleline` property"""

            return self._singleline

        @property
        def multiline(self) -> MultilineComment:
            """Getter for `multiline` property"""

            return self._multiline

    class Style(Enum):
        """Enumeration defining comment styles"""

        SINGLELINE = "singleline"
        MULTILINE = "multiline"

        @staticmethod
        def from_str(string: str) -> Optional["CommentRule.Style"]:
            """Creates a comment style from string representation.

            Returns:
                Optional[CommentRule.Style]: The style of the comment.
            """

            try:
                return CommentRule.Style(string)
            except ValueError:
                pass

            return None

    def parse(
        self,
        rule_dict: Dict[str, Any],
        rule_callback: Callable[[Optional[Context], Any], str],
        context: Optional[Context] = None,
    ) -> str:
        """Parse the rule dictionary to generate comment text.

        Args:
            rule_dict (Dict[str, Any]): The dictionary of rules.
            rule_callback (Callable[[Optional[Context], Any], str]): Callback function
                for rules not handled by the current rule.
            context (Optional[Context], optional): The context for the rule. Defaults to None.

        Returns:
            str: The generated comment text.
        """

        if context is None:
            raise NoneValueException("Param `context` must not be None")

        context_case: CommentRule.ContextCase = context.get(CommentRule.CONTEXT_NAME)
        if not isinstance(context_case, CommentRule.ContextCase):
            raise InvalidTypeException(
                f"Invalid {type(context_case)} type for {CommentRule.CONTEXT_NAME} in context",
            )

        _, style_str = self._style(rule_dict)
        style = CommentRule.Style.from_str(style_str)
        if not style:
            style = CommentRule.Style.SINGLELINE

        _, comment = self._comment(rule_dict)
        if comment is None:
            raise NoneValueException("`comment` rule is invalid")

        comment_prefix = ""
        comment_open = ""
        comment_close = ""
        if style == CommentRule.Style.SINGLELINE:
            if context_case.singleline is None:
                raise NoneValueException(
                    f"Not found {CommentRule.ContextCase.SinglelineComment.__name__} \
                    from context"
                )

            prefix = context_case.singleline.prefix
            if not isinstance(prefix, str):
                raise InvalidTypeException(
                    f"Invalid prefix from context of {CommentRule.ContextCase.__name__} \
                    `{CommentRule.CONTEXT_NAME}`"
                )
            comment_prefix = prefix

        if style == CommentRule.Style.MULTILINE:
            if context_case.multiline is None:
                raise NoneValueException(
                    f"Not found {CommentRule.ContextCase.MultilineComment.__name__} \
                    from context"
                )

            comment_prefix = context_case.multiline.prefix
            comment_open = context_case.multiline.open_comment
            comment_close = context_case.multiline.close_comment

        rules_str = ""
        if isinstance(comment, dict):
            rules_str = rule_callback(context, comment)
            rules_str = rules_str.replace("\n", f"\n{comment_prefix}")
        elif isinstance(comment, str):
            rules_str = comment
            rules_str = rules_str.replace("\n", f"\n{comment_prefix}")
        elif isinstance(comment, list):
            rules_str = [rule_callback(context, rule) for rule in comment]
            rules_str = "\n".join(rules_str).replace("\n", f"\n{comment_prefix}")
        else:
            raise InvalidTypeException("`comment` rule is an invalid type")

        output = comment_prefix + rules_str

        if comment_open:
            output = comment_open + "\n" + output

        if comment_close:
            output += "\n" + comment_close

        return output
