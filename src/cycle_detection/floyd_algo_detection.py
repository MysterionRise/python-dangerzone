from node import Node, generate_linked_list


def detect_cycle(head_node: Node) -> bool:
    slow = head_node
    fast = head_node
    loop = False

    while (
        slow is not None
        and fast is not None
        and fast.get_next_node() is not None
    ):
        slow = slow.get_next_node()
        fast = fast.get_next_node().get_next_node()

        if slow == fast:
            loop = True
            break

    if loop:
        #     we detected loop, let's find cycle length
        slow = head_node
        while slow != fast:
            slow = slow.get_next_node()
            fast = fast.get_next_node()

        print(slow.get_data())

        cycle_length = 0
        fast = slow.get_next_node()

        while slow != fast:
            fast = fast.get_next_node()
            cycle_length += 1

        print(cycle_length)

    return loop


if __name__ == "__main__":
    head = generate_linked_list(100, 0.1)
    print(detect_cycle(head))
