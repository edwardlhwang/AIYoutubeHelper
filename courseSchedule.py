class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = defaultdict(list)

        for prereq in prerequisites:
            graph[prereq[0]].append( prereq[1])
        
        print(graph)
        visitSet = set()
        def dfs(course):
            if course in visitSet:
                return False
            if course not in graph or graph[course] == []:
                return True
            visitSet.add(course)
            for preq in graph[course]:
                if not dfs(preq):
                    return False
            graph[course] = []
            visitSet.remove(course)
            return True

        for c in range(numCourses):
            if not dfs(c):
                return False

        
        return True


