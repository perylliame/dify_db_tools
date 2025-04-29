import json
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from sql_utils.sql import sql_service
from sql_utils.utils import format_json_string


class DifyDbToolsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        db_host = tool_parameters.get('db_host')
        db_user = tool_parameters.get('db_user')
        db_password = tool_parameters.get('db_password')
        db_database = tool_parameters.get('db_database')
        db_port = int(tool_parameters.get('db_port'))

        connect_config = {
            "host": db_host,
            "user": db_user,
            "password": db_password,
            "database": db_database,
            "port": db_port,
        }

        print(connect_config)

        # module_config = DEMO_MODULE_CONFIG

        operate_type = tool_parameters.get('operateType')

        if operate_type is None:
            yield self.create_json_message({
                "error": "operateType is required"
            })
            return

        operate_data = None
        operate_data_str = tool_parameters.get('operateData')

        if operate_data_str is None:
            yield self.create_json_message({
                "error": "operateData is required"
            })
            return

        try:
            operate_data_str = format_json_string(operate_data_str)
            operate_data = json.loads(operate_data_str)
        except json.JSONDecodeError:
            yield self.create_json_message({
                "error": "decode operateData failed",
                "operate_data_str": operate_data_str,
            })
            return

        module_config = None
        module_config_str = tool_parameters.get('moduleConfig')

        if module_config_str is None:
            yield self.create_json_message({
                "error": "moduleConfig is required"
            })
            return

        try:
            module_config_str = format_json_string(module_config_str)
            module_config = json.loads(module_config_str)
        except json.JSONDecodeError:
            yield self.create_json_message({
                "error": "decode moduleConfig failed",
                "module_config_str": module_config_str,
            })
            return

        print({
            "module_config": type(module_config),
            "operate_data": type(operate_data),
            "operate_type": type(operate_type),
        })

        operate_result = None
        debug_data = []

        if operate_type == 'query':
            operate_result = sql_service['select'](
                connect_config=connect_config,
                query_config=operate_data,
                module_config=module_config,
                debug_data=debug_data,
            )
        elif operate_type == 'item':
            operate_result = sql_service['select_one'](
                connect_config=connect_config,
                query_config=operate_data,
                module_config=module_config,
                debug_data=debug_data,
            )
        elif operate_type == 'insert':
            operate_result = sql_service['insert'](
                connect_config=connect_config,
                query_config=operate_data,
                module_config=module_config,
                debug_data=debug_data,
            )
        elif operate_type == 'update':
            operate_result = sql_service['update'](
                connect_config=connect_config,
                query_config=operate_data,
                module_config=module_config,
                debug_data=debug_data,
            )
        elif operate_type == 'delete':
            operate_result = sql_service['delete'](
                connect_config=connect_config,
                query_config=operate_data,
                module_config=module_config,
                debug_data=debug_data,
            )
        elif operate_type == 'batchInsert':
            operate_result = sql_service['batch_insert'](
                connect_config=connect_config,
                query_config=operate_data,
                module_config=module_config,
                debug_data=debug_data,
            )
        elif operate_type == 'batchUpdate':
            operate_result = sql_service['batch_update'](
                connect_config=connect_config,
                query_config=operate_data,
                module_config=module_config,
                debug_data=debug_data,
            )
        else:
            operate_result = {"error": f"Can't recognise operate type: {operate_type}"}

        print('operate_result=====>>\n\n', operate_result)
        yield self.create_json_message(operate_result)
