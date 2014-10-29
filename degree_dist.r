library(igraph)
library(kitagawa)

minor.ticks.axis <- function(ax,n,t.ratio=0.5,mn,mx,...){
  
  lims <- par("usr")
  if(ax %in%c(1,3)) lims <- lims[1:2] else lims[3:4]
  
  major.ticks <- pretty(lims,n=5)
  if(missing(mn)) mn <- min(major.ticks)
  if(missing(mx)) mx <- max(major.ticks)
  
  major.ticks <- major.ticks[major.ticks >= mn & major.ticks <= mx] 
  
  labels <- sapply(major.ticks,function(i) {
      as.expression(bquote(10^ .(i)))
    })
  axis(ax,at=10 ^major.ticks,labels=labels,...)
  
  n <- n+2
  minors <- log10(pretty(10^major.ticks[1:2],n)) - major.ticks[1]
  minors <- minors[-c(1,n)]
  
  minor.ticks = c(outer(minors,major.ticks,`+`))
  minor.ticks <- minor.ticks[minor.ticks > mn & minor.ticks < mx]
  
  axis(ax,at=10^minor.ticks,tcl=par("tcl")*t.ratio,labels=FALSE)
}

b <- read.graph('debatenaglobo_graph.net', format='pajek')

pdf('degree.pdf', width=4.75, height=4.75)

plot(degree.distribution(b), 
     cex=.75, 
     log='xy', 
     xlab='k', 
     ylab='P(k)',
     yaxt='n',
     xaxt='n',
     ylim=c(0.00001, 1.0),
     xlim=c(1.0, 100000.0))

#aty <- axTicks(2)
aty <- c(1e-05, 1e-04, 1e-03, 1e-02, 1e-01, 1e-00)
atx <- c(1e00, 1e01, 1e02, 1e03, 1e04, 1e05)
#atx <- axTicks(1)
labelsy <- sapply(aty,function(i)
  as.expression(bquote(10^ .(log(i, 10))))
)
labelsx <- sapply(atx,function(i)
  as.expression(bquote(10^ .(log(i, 10))))
)
axis(2,at=aty,labels=labelsy)
#axis(1,at=atx,labels=labelsx)

abline(1, -2.5, lty=2)

minor.ticks.axis(1,9,mn=0,mx=5)
minor.ticks.axis(2,9,mn=-5,mx=0)

dev.off()
