
pdf('tweet_acc.pdf', width=4.75, height=4.75)

attach(mtcars)
par(mfrow=c(1,2))

r <- read.table('activity.table')
x <- r[r$V1 >= 900 & r$V1 <= 1010,]
plot((cumsum(x$V2) / max(cumsum(x$V2))) ~ x$V1, 
     type='l',
     ylab="Frequência acumulada de tuítes",
     xlab="Horário",
     xaxt='n')
axis(1, 
     at = axTicks(1), 
     labels = c("22:00", "22:20", "22:40", "", "23:20", "23:50"))
abline(v=955)
grid()

r <- read.table('activity.retweet.table')
x <- r[r$V1 >= 900 & r$V1 <= 1010,]
plot((cumsum(x$V2) / max(cumsum(x$V2))) ~ x$V1, 
     type='l',
     ylab="Frequência acumulada de retuítes",
     xlab="Horário",
     xaxt='n')
axis(1, 
     at = axTicks(1), 
     labels = c("22:00", "22:20", "22:40", "", "23:20", "23:50"))
abline(v=955)
grid()

dev.off()
