import ast
import asyncio

import colorama

from domain.graph import Graph
from use_cases import construct_graph, print_graph


class ConsoleProgram:
    def __init__(self):
        self.graph = None

        colorama.init(autoreset=True)

    def display_menu(self):
        print("1. Create graph")
        print("2. Print graph")
        print("3. Print execution order")
        print("4. Exit")

    def create_graph(self):
        input_string = input("Enter the list of edges: ")
        try:
            edges = ast.literal_eval(input_string)
            self.graph = construct_graph.create_graph_from_directional_edges(
                edges
            )
        except (SyntaxError, ValueError):
            print(colorama.Fore.RED + "Invalid input.")

    def print_graph(self):
        if self.graph is None:
            print(colorama.Fore.RED + "Graph is not created")
            return

        print_graph.print_graph(self.graph)

    def print_execution_order(self):
        if self.graph is None:
            print(colorama.Fore.RED + "Graph is not created")
            return

        asyncio.run(print_graph.print_execution_order(self.graph))

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter choice: ")

            if choice == "1":
                self.create_graph()
                print("\n", end="")
            elif choice == "2":
                self.print_graph()
                print("\n", end="")
            elif choice == "3":
                self.print_execution_order()
                print("\n", end="")
            elif choice == "4":
                break
            else:
                print(colorama.Fore.RED + "Invalid choice")


if __name__ == "__main__":
    program = ConsoleProgram()
    program.run()
