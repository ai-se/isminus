class Search:

    @staticmethod
    def bfs(tree, target):
        # maintain a queue of paths
        queue = [[tree]]
        # push the first path into the queue
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            path_id = [x.id for x in path]
            # get the last node from the path
            node = path[-1]
            if node.east:
                # path found
                if target == node.score:
                    return path_id, node
                # enumerate all adjacent nodes, construct a new path and push it into the queue
                neighbors = []
                if node.west_node:
                    neighbors.append(node.west_node)
                if node.east_node:
                    neighbors.append(node.east_node)
                for adjacent in neighbors:
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)

    @staticmethod
    def bfsFinal(tree, target):
        # maintain a queue of paths
        queue = [[tree]]
        # push the first path into the queue
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            path_id = [x.id for x in path]
            # get the last node from the path
            node = path[-1]
            if node.east:
                # path found
                if target == node.weight and node.leaf:
                    return path_id, node
                # enumerate all adjacent nodes, construct a new path and push it into the queue
                neighbors = []
                if node.west_node:
                    neighbors.append(node.west_node)
                if node.east_node:
                    neighbors.append(node.east_node)
                for adjacent in neighbors:
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)

    @staticmethod
    def get_all_items(tree):
        # maintain a queue of paths
        queue = [[tree]]
        results = []
        # push the first path into the queue
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            path_id = [x.id for x in path]
            # get the last node from the path
            node = path[-1]
            if node.east:
                # path found
                if 1 == node.weight and node.leaf:
                    items = [x for x in node.east]
                    for item in items:
                        results.append(item)
                # enumerate all adjacent nodes, construct a new path and push it into the queue
                neighbors = []
                if node.west_node:
                    neighbors.append(node.west_node)
                if node.east_node:
                    neighbors.append(node.east_node)
                for adjacent in neighbors:
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)
        return results

    @staticmethod
    def get_all_leaves(tree):
        # maintain a queue of paths
        queue = [[tree]]
        results = []
        # push the first path into the queue
        while queue:
            # get the first path from the queue
            path = queue.pop(0)
            path_id = [x.id for x in path]
            # get the last node from the path
            node = path[-1]
            if node.east:
                # path found
                if node.leaf:
                    items = [x for x in node.east]
                    for item in items:
                        results.append(item)
                # enumerate all adjacent nodes, construct a new path and push it into the queue
                neighbors = []
                if node.west_node:
                    neighbors.append(node.west_node)
                if node.east_node:
                    neighbors.append(node.east_node)
                for adjacent in neighbors:
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)
        return results

    @staticmethod
    def get_item(tree, path):
        # maintain a queue of paths
        cur = tree
        for val in path[1:-1]:
            if cur.east_node.id == val:
                cur = cur.east_node
            elif cur.west_node.id == val:
                cur = cur.west_node
        last = path[-1]
        if cur.east_node.id == last:
            return cur.east[0].item
        elif cur.west_node.id == last:
            return cur.west[0].item
