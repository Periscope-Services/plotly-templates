library(ggplot2) 
library(plotly)

# ggplot object, non-interactive
p=ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width, color=Species, shape=Species)) + 
    geom_point(size=6, alpha=0.6)

# plotly object!
p <- ggplotly(p)

periscope.plotly(ggplotly(p))