class Tree(object):
  root = None
  unordered_nodes = None

  def __init__(self, root):
    self.root = root
    self.unordered_nodes = set()

  def add_node(self, node, parent=None):
    self.unordered_nodes.add(node)
    if parent:
      parent.add_child(node)

  def get_node(self, value):
    for node in self.unordered_nodes:
      if node.value == value:
        return node
    return None

  def get_or_create_node(self, value):
    node = self.get_node(value)
    return node if node else Node(value)

  def select_root(self):
    for node in self.unordered_nodes:
      if any([node in n.children for n in self.unordered_nodes]):
        continue
      self.root = node
      return node
    raise Exception('ISGRAPH')


class Node(object):
  value = None
  children = None

  def __init__(self, value):
    self.value = value
    self.children = set()

  def add_child(self, child):
    self.children.add(child)


def count_tree_nodes(tree):
  return count_children(tree.root)


def count_children(node):
  child_num = len(node.children) + 1
  for n in node.children:
    child_num += count_children(n)
  return child_num


def main():
  data = open('./data/day6.txt').read().split('\n')
  t = Tree(None)
  for line in data:
    orbited, orbiting = [t.get_or_create_node(name) for name in line.split(')')]
    t.add_node(orbited)
    t.add_node(orbiting, orbited)
  t.select_root()

  print(count_tree_nodes(t))


main()
