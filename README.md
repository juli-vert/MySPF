# MySPF
Python SPF implementation based in a full graph walk-through 

Routing using the MySPF implementation

Based on a central controller which retrieves/maintains information about the network.
The Controller calculates all the best routes and push the subset of routes to each vertex/router
New Routers are announced themselves
Adding new edges between routers are pushed from the controller
Removing edges between routers are pushed from the controller
