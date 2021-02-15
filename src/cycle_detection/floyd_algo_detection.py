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
    return loop


if __name__ == "__main__":
    head = generate_linked_list(100, 0.01)
    print(detect_cycle(head))
