#Example from online
# Libraries
library(ggplot2)
library(dplyr)
library(hrbrthemes)

# Load dataset from github
#data <- read.table("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/1_OneNum.csv", header=TRUE)
require(dplyr)
require(hrbrthemes)
# Make the histogram

#Set work directory to Rust location
setwd("F:/RustCalc")
getwd()

data<- read.csv("test.csv", header=TRUE)

head(data)



Moneyhead<-as.numeric(data$Money.spent[1001:2000])
Moneytail<-as.numeric(data$Money.spent[9000:8001])

Moneyhead

MONEY<-data.frame(
  Money = c(Moneyhead,Moneytail),
  Simulation = rep(c("Simulation 1","Simulation 2"), each=length(Moneyhead))
  
)

library(ggplot2)
ggplot(MONEY, aes(x=Money, fill = Simulation)) + geom_density(color="#e9ecef",alpha=0.5)+
  ggtitle("Simulation comparison") +
  theme_ipsum()


# Kolmogorov-Smirnov test ####
results<-ks.test(Moneyhead, Moneytail)

results$p.value



install.packages("sm")
library(sm)
sm.density.compare(MONEY$Money, MONEY$Simulation, model = "equal", nboot=500, ngrid=100)





library(CDFt)
library(fitdistrplus)
png("Simulation 1 distribution.png", 720,480)
descdist(data =MONEY$Money,discrete = FALSE,boot=1000)


ks.test(MONEY$Money,"plnorm")
ks.test(MONEY$Money,"gamma")

fg <- fitdist(MONEY$Money, "gamma")
fln <- fitdist(MONEY$Money, "lnorm")
fw <- fitdist(MONEY$Money, "weibull")
par(mfrow = c(2, 2))
plot.legend <- c("Weibull", "lognormal", "gamma")
denscomp(list(fw, fln, fg), legendtext = plot.legend)
qqcomp(list(fw, fln, fg), legendtext = plot.legend)
cdfcomp(list(fw, fln, fg), legendtext = plot.legend)
ppcomp(list(fw, fln, fg), legendtext = plot.legend)

fexp<-fitdist(MONEY$Money, "exp")
plot(fexp)


plot(fw)
