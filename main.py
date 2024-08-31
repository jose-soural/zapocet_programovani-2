import argparse
from functions import *


# ================
# "Monkey patching" the behaviour of --help in argparse to NOT exit the program after displaying help:
class CustomHelpAction(argparse._HelpAction):
    # Override the problematic method
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        # parser.exit()
        print("Help displayed. Continuing program execution.")


argparse._HelpAction = CustomHelpAction
# =================


def casefold(string):
    return string.casefold()


def make_name(underscored_string):
    return ' '.join([word for word in underscored_string.split(separator="_")])


def make_description(word_list):
    return ' '.join(word_list)


# The parser for when the user starts the program
entry_parser = argparse.ArgumentParser(prog="TO-DO-IQ",
                                       description="An intelligent TO-DO list, utilises the python argparse module. Supports a wide variety of task"
                                                   "frequencies and handles automatic renewing of tasks.",
                                       epilog="----------\nHelp displayed. Continuing execution."
                                       )
# One subparser for each end-user function
commands = entry_parser.add_subparsers(title="Available commands:", required=True, dest="command")

p_save = commands.add_parser("save_changes", aliases=['sc', 'save'], help="Saves all changes and progress made to all tasks as well as programme configurations.")
p_save.set_defaults(func=save_changes)

p_exit = commands.add_parser("exit", help="Properly saves all changes made and exits the programme.")
p_exit.set_defaults(func=exit_programme)

p_abort = commands.add_parser("exit_without_saving", aliases=['ews', 'es', 'abort'], help="Properly exits the programme WITHOUT saving the changes made to the tasks and programme configurations.")
p_abort.set_defaults(func=exit_without_saving)

p_create = commands.add_parser("create_task", aliases=['ct', 'create'], help="Creates a task with the given name, frequency (= trigger condition), description and status & adds it to appropriate lists.")
p_create.add_argument("task_name", type=make_name, help="The name of the task to be created. Underscores ('_') will be turned into spaces.")
p_create.add_argument("frequency", default="once", help="The frequency (trigger condition) of the task to be created. See or list_frequencies command for a list of all valid frequencies.")
p_create.add_argument("--description", "-d", nargs="*", default="", type=make_description, help="A more detailed description of the task to be.")
p_create.add_argument("status", type=casefold, choices=["due", "overdue", "asleep", "finished"], default="due", help="The starting status of the task to be.")
p_create.set_defaults(func=_create_task_argparse)

p_list_freq = commands.add_parser("list_frequencies", aliases=['lf'], help="Displays a list of all valid task frequencies (= trigger conditions).")
p_list_freq.set_defaults(func=list_valid_frequencies)

p_delete = commands.add_parser("delete_task", aliases=['dt', 'delete'], help="Deletes the specified task.")
p_delete.add_argument("target_task", nargs="+", type=make_description, help="The task to be deleted. Can be its name or its index as listed in the last displayed list.")
p_delete.set_defaults(func=delete_task)

p_rename = commands.add_parser("rename_task", aliases=['rt', 'rename', "change_name", "cn"], help="Changes the name of the specified task.")
p_rename.add_argument("target_task", nargs="+", type=make_description, help="The task to undergo name change. Can be its name or its index as listed in the last displayed list.")
p_rename.add_argument("--new", "-n", required=True, type=make_name, help="The new name for the task. Underscores ('_') will be turned into spaces.")
p_rename.set_defaults(func=change_name)

p_refreq = commands.add_parser("change_frequency", aliases=["cf", "change_freq"], help="Changes the frequency of the specified task.")
p_refreq.add_argument("target_task", nargs="+", type=make_description, help="The task to undergo frequency change. Can be its name or its index as listed in the last displayed list.")
p_refreq.add_argument("--new", "-n", required=True, help="The new frequency for the task.")
p_refreq.set_defaults(func=change_frequency)

p_redescr = commands.add_parser("change_description", aliases=["cd", "change_descr"], help="Changes the description of the specified task.")
p_redescr.add_argument("target_task", nargs="+", type=make_description, help="The task to undergo description change. Can be its name or its index as listed in the last displayed list.")
p_redescr.add_argument("--new", "-n", nargs="*", type=make_description, help="The new description for the task.")
p_redescr.set_defaults(func=change_description)

p_set_asleep = commands.add_parser("set_asleep", aliases=["sa", "asleep", "sleep"], help="Sets the task to 'sleep' making become due on a specific day. Note: this makes it ignore its normal trigger condition.")
p_set_asleep.add_argument("target_task", nargs="+", type=make_description, help="The task to be put to sleep. Can be its name or its index as listed in the last displayed list.")
p_set_asleep.set_defaults(func=set_asleep)

p_set_due = commands.add_parser("make_due", aliases=["md", "renew", "set_due", "sd"], help="Sets a task's status to 'due' and ads it to the agenda.")
p_set_due.add_argument("target_task", nargs="+", type=make_description, help="The task to be put to renewed. Can be its name or its index as listed in the last displayed list.")
p_set_due.set_defaults(func=renew)

p_set_overdue = commands.add_parser("mark_as_overdue", aliases=["mao", "mo", "set_overdue", "so"], help="Sets a task's status to 'overdue', marking its completion as high priority.")
p_set_due.add_argument("target_task", nargs="+", type=make_description, help="The task to be put to made overdue. Can be its name or its index as listed in the last displayed list.")
p_set_due.set_defaults(func=mark_as_overdue)

p_set_fin = commands.add_parser("finish", aliases=["fin", "make_finished", "mf"], help="Sets a task's status to 'finished', marking its completion and taking it off the agenda. NOTE: finishing a 'once' task will automatically remove it")
p_set_fin.add_argument("target_task", nargs="+", type=make_description, help="The task to be put to made overdue. Can be its name or its index as listed in the last displayed list.")
p_set_fin.set_defaults(func=finish)

p_descr = commands.add_parser("description", aliases=["descr"], help="Displays the description of the task.")
p_descr.add_argument("target_task", nargs="+", type=make_description, help="The task whose description is to be shown. Can be its name or its index as listed in the last displayed list.")
p_descr.set_defaults(func=description)

p_detail = commands.add_parser("detail", help="Displays all information about the task.")
p_detail.add_argument("target_task", nargs="+", type=make_description, help="The task whose information is to be shown. Can be its name or its index as listed in the last displayed list.")
p_detail.set_defaults(func=detail)

p_disp_all = commands.add_parser("display_all", aliases=["da"], help="Displays all (optionally only finished) tasks currently logged by the programme. Please note that this may be demanding on your device.")
p_disp_all.add_argument("--finished", "-f", action="store_true", help="Toggles whether to display only finished tasks.")
p_disp_all.set_defaults(func=display_all)

p_disp_list = commands.add_parser("display_list", aliases=["dl", "display", "disp"], help="Displays all tasks (their names) of the specified frequency and status.")
p_disp_list.add_argument("frequency", default="once", help="The frequency of the tasks to be displayed. Can be any frequency from the list_frequencies command, or 'all'.")
p_disp_list.add_argument("status", type=casefold, choices=["due", "overdue", "asleep", "finished_today", "all"], default="due", help="The status of the tasks to be displayed.")
p_disp_list.set_defaults(func=display_list)

p_disp_due = commands.add_parser("due", help="Displays all due tasks except tasks that are overdue.")
p_disp_due.set_defaults(func=_display_list_argparse)

p_disp_overdue = commands.add_parser("overdue", help="Displays all overdue tasks.")
p_disp_overdue.set_defaults(func=_display_list_argparse)

p_disp_asleep = commands.add_parser("asleep", help="Displays all tasks which are asleep.")
p_disp_asleep.set_defaults(func=_display_list_argparse)

p_disp_ft = commands.add_parser("finished_today", aliases=["ft"], help="Displays all tasks which were finished today.")
p_disp_ft.set_defaults(func=_display_list_argparse)

p_to_do = commands.add_parser("to_do", aliases=["td", "todo", "to-do", "today"], help="Displays all tasks on today's agenda.")
p_to_do.set_defaults(func=to_do)

p_refresh = commands.add_parser("refresh_to_do", aliases=["rtd", "refresh"], help="Updates the to-do list. Based on the system date, it wakes up sleepers, adds due tasks and potentially marks tasks that are overdue.")
p_refresh.set_defaults(func=refresh_to_do)

p_config = commands.add_parser("change_configurations", aliases=["cc", "change_config", "config"], help="Change program configurations.")
settings = p_config.add_mutually_exclusive_group(required=True)
settings.add_argument("--auto_refresh", type=casefold, choices=["true", "false"], help="Toggle whether you want the program to automatically refresh the to-do list upon booting. (Default = False)")
p_config.set_defaults(func=change_config)


def main():
    print("Welcome to TO-DO-IQ! Type in a valid command to continue. Type --help for help.")
    while True:
        try:
            namespace = entry_parser.parse_args()
            namespace.func(namespace)
        except SystemExit() as e:
            if e.code == 2:
                pass        # Argparse berated the user, we can continue
            elif e.code == 0:       # The user wants to exit via the python built-in commands
                _catch_close_command()
            elif e.code == 42:       # Built in exit procedure
                print("Graceful shutdown successful. Until next time!")
                break
            else:                   # Something went horribly wrong
                raise
        except (KeyboardInterrupt, EOFError):
            _catch_close_command()


if __name__ == "__main__":
    main()
