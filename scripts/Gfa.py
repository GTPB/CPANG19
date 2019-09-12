#!/usr/bin/python

class Node:
	def __init__(self):
		self.nodeid = 0
		self.nodeseq = ""
		self.length = 0
		self.readcount = 0
		self.frequency = 0
		self.chain = None

def reverse(pos):
	return ((pos[0], not pos[1]))

class Graph:
	def _parse_node(self, parts):
		result = Node()
		result.nodeid = parts[1]
		result.nodeseq = parts[2]
		result.length = 0
		result.readcount = 0
		result.frequency = 0
		for tag in parts[3:]:
			if tag[0:5] == 'LN:i:':
				result.length = int(tag[5:])
			elif tag[0:5] == 'RC:i:':
				result.readcount = int(tag[5:])
			elif tag[0:5] == 'km:f:':
				result.frequency = float(tag[5:])
		return result
	def __init__(self):
		self.nodes = {}
		self.edges = {}
	def load(self, filename):
		with open(filename) as f:
			for l in f:
				parts = l.strip().split('\t')
				if parts[0] == 'S':
					parsed = self._parse_node(parts)
					self.nodes[parsed.nodeid] = parsed
					if (parts[1], True) not in self.edges: self.edges[(parts[1], True)] = set()
					if (parts[1], False) not in self.edges: self.edges[(parts[1], False)] = set()
				if parts[0] == 'L':
					frompos = (parts[1], parts[2] == '+')
					topos = (parts[3], parts[4] == '+')
					overlap = int(parts[5][:-1])
					if frompos not in self.edges: self.edges[frompos] = set()
					if reverse(topos) not in self.edges: self.edges[reverse(topos)] = set()
					readcount = None
					for tag in parts[6:]:
						if tag[0:5] == "RC:i:": readcount = float(tag[5:])
					self.edges[reverse(topos)].add((reverse(frompos), (overlap, readcount)))
					self.edges[frompos].add((topos, (overlap, readcount)))
	def remove_nonexistent_edges(self):
		extra = []
		for edge in self.edges:
			if edge[0] not in self.nodes:
				extra.append(edge)
				continue
			extra_here = []
			for target in self.edges[edge]:
				if target[0][0] not in self.nodes:
					extra_here.append(target)
					continue
			for e in extra_here:
				self.edges[edge].remove(e)
		for e in extra:
			del self.edges[e]
	def write(self, filename):
		with open(filename, 'w') as f:
			for node in self.nodes:
				n = self.nodes[node]
				line = "S\t" + str(n.nodeid) + "\t" + n.nodeseq + "\tLN:i:" + str(n.length)
				if n.readcount: line += '\tRC:i:' + str(n.readcount)
				if n.length: line += '\tkm:f:' + str(float(n.readcount)/float(n.length))
				if n.chain: line += "\tbc:Z:" + str(n.chain)
				f.write(line + '\n')
			for edge in self.edges:
				for target in self.edges[edge]:
					line = "L\t" + str(edge[0]) + "\t" + ("+" if edge[1] else "-") + "\t" + str(target[0][0]) + '\t' + ("+" if target[0][1] else "-") + '\t' + str(target[1][0]) + 'M'
					if target[1][1]:
						line += "\tRC:i:" + str(target[1][1])
					f.write(line + '\n')
