t <- read.table('activity.all.table')
r <- t[t$V1 > 850 & t$V1 < 1100,]

t2 <- read.table('activity.table')
r2 <- t2[t2$V1 > 850 & t2$V1 < 1100,]

debate <- t[t$V1 > 900 & t$V1 < 1010,]
summary(debate)

pdf(width=6.47, height=4.71, file = "activity.pdf")

plot(r, type='l', ylab='Tuítes', xlab='Horário', xaxt='n')

lines(r2, lty=2)

title("#DebateNaGlobo")
l <- c("21:10", "", "21:50", "", "22:30", "", "23:10", "", "23:50", "", "00:30", "", "01:10")
axis(1, at=seq(850, 1100, 20), labels=l)

legend('topright', c("Total", 'Retuítes'), 
       lty=c(1, 2), bty='n', cex=.75)

dev.off()
