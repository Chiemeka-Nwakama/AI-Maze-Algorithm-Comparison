# Comparative Analysis of Pathfinding Algorithms Online DFS and Directed Online DFS on Grid World

The Grid World problem type requires a pathfinding algorithm to navigate an agent from a start to a goal node on a
grid. The choice of algorithm impacts the agent’s route and
computational efficiency. This study compared the Online
Depth First Search (Online DFS) algorithm with a directed
variant of this algorithm for Grid World based on processing time and spaces explored. The Online DFS algorithm
performs a depth-first search to incrementally discover a
path to the goal. The directed version incorporates heuristic
guidance on exploration direction. The comparison was conducted on a 25x25 square grid with a randomized layout each
time, forcing the agent to explore a new environment. By
running both algorithms on identical Grid World instances,
the time elapsed before the goal node was reached was measured, alongside tallying the number of grid spaces explored
during computation. Results provide insight into the tradeoffs of informed directional guidance versus more flexible
exploratory behavior when solving randomized 25x25 Grid
World layouts. Findings discuss which algorithm more efficiently solves Grid World across the measured metrics. This
supports the selection of the superior approach for pathplanning applications.
K
