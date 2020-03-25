#!/usr/bin/env python
from monkey import Monkey
import time
import argparse
import sys
import json
from cmd import Cmd


class MonkeyCLI(Cmd):

    prompt = 'monkey> '
    monkey = Monkey()
    history = []
    history_index = 0

    def __init__(self):
        super().__init__()
        if len(sys.argv) > 1:
            self.parse_args(sys.argv[1:])
            exit(0)

    def do_exit(self, inp):
        '''exit the application.'''
        print("Bye")
        return True

    def do_help(self, inp):
        self.parse_args(["--help"])

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
 
        print("Default: {}".format(inp))
        self.parse_args(inp.split(" "))

    def create_instance(self, provider, machine_overrides):
        print("Creating Instance with override args:\n{}".format(machine_overrides))
        return self.monkey.create_instance(provider= provider, machine_params=machine_overrides)        

    def list_providers(self, printout=False):
        if printout:
            print('''
Listing Providers available
                ''')
        providers = []
        for handler in self.monkey.handlers:
            if printout:
                print("{}".format(handler))
            providers.append(handler.name)
        return providers

    def list_jobs(self, providers, printout=False):
        if printout:
            print('''
Listing Jobs available
                ''')
        print(providers)
        jobs = []
        for handler in self.monkey.handlers:
            if handler.name in providers:
                jobs += handler.list_jobs()

        if printout:
            print('''
Found Jobs:
{}            
        '''.format(',\n'.join(jobs)))
        return jobs

    def parse_args(self, input_args):
        print("Parsing args: {}".format(input_args))
        parser = argparse.ArgumentParser(description='Parses monkey commands')

        subparser = parser.add_subparsers(help="Monkey Commands", dest="command")

        run_parser = subparser.add_parser("run", help="Run a job on the specified provider")
        
        create_parser = subparser.add_parser("create", help="Create an instance on the specified provider")
        create_subparser = create_parser.add_subparsers(description="Create command options", dest="create_option")
        create_instance_parser = create_subparser.add_parser("instance", help="Creates an instance with given provider and overrides")
        create_instance_parser.add_argument('-p','--provider', dest='provider', type=str, required=True,
                         help='The provider you wish to use.  Should be defined in cloud_providers.yaml')
        # create_instance_parser.add_argument('machine_params', type=str, nargs=argparse.REMAINDER,
        #                  help='Any other machine overrides to replace values found in cloud_providers.yaml')


        list_parser = subparser.add_parser("list", help="List jobs on the specified provider")
        list_subparser = list_parser.add_subparsers(description="List command options", dest="list_option")
        list_jobs_parser = list_subparser.add_parser("jobs", help="List the jobs on the given provider")
        list_providers_parser = list_subparser.add_parser("providers", help="List the jobs on the given provider")
        list_jobs_parser.add_argument('-p','--providers', dest='providers', type=str, required=False, nargs="*", default=None,
                         help='The provider you wish to use.  Should be defined in cloud_providers.yaml')

        info_parser = subparser.add_parser("info", help="Infoon the specified item")
        info_subparser = info_parser.add_subparsers(description="Info options", dest="info_option")
        info_jobs_parser = list_subparser.add_parser("job", help="Gets the info on the specified job")
        info_providers_parser = list_subparser.add_parser("instance", help="List the info of the specified instance")


        try:
            args, remaining_args = parser.parse_known_args(input_args)
        except:
            return False
        if args.command == "run":
            pass
        elif args.command == "create":
            if args.create_option == "instance":
                additional_args = dict()
                provider = args.provider
                if len(remaining_args):
                    print("Adding override argumen: \n")
                for i in range(0, len(remaining_args), 2):
                    if remaining_args[i][:2] == "--":
                        print("{}={}".format(remaining_args[i][2:], remaining_args[i + 1]))
                        additional_args[remaining_args[i][2:]] = remaining_args[i+1]
                
                return self.create_instance(provider=args.provider, machine_overrides=additional_args)
            else:
                create_parser.print_help()
                return False
        elif args.command == "list":
            if args.list_option == "jobs":
                if args.providers is not None:
                    self.list_jobs(providers=args.providers, printout=True)
                else:
                    self.list_jobs(providers=self.list_providers(), printout=True)
            elif args.list_option == "providers":
                return self.list_providers(printout=True)
            else:
                list_parser.print_help()
                return False
        else:
            parser.print_help()
            return False


        # parser.add_argument('command', help='Subcommand to run')
        # args = parser.parse_args(input_args[1:2])
        # if not hasattr(args, "command"):
        #     print('Unrecognized command')
        #     parser.print_help()
        #     exit(1)
        # # use dispatch pattern to invoke method with same name
        # print(getattr(args, "command"))
        # command = getattr(args, "command")
        # getattr(self, command)(input_args[2:])

        return args

def main():
    MonkeyCLI().cmdloop()

    return 0

if __name__ == "__main__":
    exit(main())