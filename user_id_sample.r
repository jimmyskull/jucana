
library(igraph)

giant.component <- function(graph) {
  cl <- clusters(graph)
  induced.subgraph(graph, which(cl$membership == which.max(cl$csize)))
}

s <- read.graph('sampled_graph.net', format='pajek')

g <- giant.component(as.undirected(s))

vlogsize <- log(V(g)$vertexsize)
vsizes <- (vlogsize / max(vlogsize)) * 3.0

ewidth <- E(g)$weight

#pdf("sample.pdf", width=3.45, height=3.45)
pdf("sample.pdf", width=10, height=10)

plot(g, 
     vertex.size=vsizes, 
     vertex.label=NA, 
     vertex.color="black",
     edge.width=ewidth,
     edge.color="SkyBlue2",
     layout=layout.fruchterman.reingold)

dev.off()
