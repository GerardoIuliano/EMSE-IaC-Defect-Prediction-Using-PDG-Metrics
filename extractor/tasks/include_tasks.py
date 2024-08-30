from __future__ import annotations

from collections.abc import Sequence

from ... import representation as rep
from ..result import ExtractionResult
from ..var_context import ScopeLevel
from .base import TaskExtractor


class IncludeTaskExtractor(TaskExtractor):

    def extract_task(self, predecessors: Sequence[rep.ControlNode]) -> ExtractionResult:
        with self.setup_task_vars_scope(ScopeLevel.INCLUDE_PARAMS):
            abort_result = ExtractionResult.empty(predecessors)

            args = dict(self.task.args)
            incl_name = args.pop('_raw_params', '')
            if not incl_name or not isinstance(incl_name, str):
                self.logger.error(f'Unknown included file name!')
                return abort_result

            if '{{' in incl_name:
                # TODO: When we do handle expressions here, we should make sure
                # to check whether these expressions can or cannot use the include
                # parameters. If they cannot, we should extract the included
                # name before registering the variables.
                self.logger.warning(f'Cannot handle dynamic file name on {self.task.action} yet!')
                return abort_result

            if args:
                # Still arguments left?
                self.logger.warning('Superfluous arguments on include/import task!')
                self.logger.debug(args)

            self.logger.debug(incl_name)
            with self.context.include_ctx.load_and_enter_task_file(incl_name, self.location) as task_file:
                if not task_file:
                    self.logger.error(f'Task file not found: {incl_name}')
                    return abort_result

                # If there's a condition on this task, the predecessors for the
                # task itself become the conditionals.
                condition_result: ExtractionResult | None = None
                if self.task.action == 'import_tasks' and self.task.when:
                    self.logger.warning('Not sure how to handle conditional on static import')
                elif self.task.when:
                    condition_result = self.extract_condition(predecessors)
                    predecessors = condition_result.next_predecessors

                self.warn_remaining_kws()

                self.logger.info(f'Following include of {task_file.file_path}')
                # Delayed import to prevent circular imports. task_files imports
                # blocks, which in turn imports this module.
                from ..task_lists import TaskListExtractor
                task_file_result = TaskListExtractor(self.context, task_file.tasks).extract_tasks(predecessors)  # type: ignore[arg-type]

            if condition_result is None:
                return task_file_result

            # If there was a condition, make sure to link up any global variables
            # defined in the task file to indicate that they're conditionally
            # defined. We also need to add _ALL_ condition nodes as potential
            # next predecessors, not just the last one, since subsequent conditions
            # may be skipped.
            for condition_node in condition_result.added_control_nodes:
                for added_var in task_file_result.added_variable_nodes:
                    self.context.graph.add_edge(condition_node, added_var, rep.DEFINED_IF)
            return task_file_result.add_control_nodes(condition_result.added_control_nodes).add_next_predecessors(condition_result.added_control_nodes)
