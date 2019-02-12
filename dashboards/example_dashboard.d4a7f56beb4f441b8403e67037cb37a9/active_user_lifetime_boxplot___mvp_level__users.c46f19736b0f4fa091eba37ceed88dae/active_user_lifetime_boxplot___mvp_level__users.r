# SQL output is imported as a dataframe variable called "df"
# Use Periscope to visualize a dataframe or show text by passing data to periscope.table() or periscope.text() respectively. Show an image by calling periscope.image() after your plot.

library(tidyverse)

# This is all Periscope theming courtesy of Christine Quan
# https://github.com/christinequan/PeriscopeR
theme_periscope <- function(
  base_size = 1,
  periscope_colors = c("#947CB0", "#663399", "#AEA8D3", "#9A12B3","#BE90D4", "#9B59B6", "#DCC6E0", "#674172", "#913D88"),
  palette = RColorBrewer::brewer.pal("Greys", n=9),
  color.background = palette[2],
  color.grid.major = palette[3],
  color.axis.text = palette[6],
  color.axis.title = palette[6],
  color.title = "#2F0035",
  color.subtitle = "#535368") 
  {
  theme_minimal() +
    theme(legend.position="none") +
    #theme(legend.text = element_text(size=1.2 * 7,color=color.axis.title)) +
    theme(legend.text = element_text(size= base_size * 7,color=color.axis.title)) +
    theme(legend.title=element_blank()) +

    theme(plot.title = element_text(color=color.title, size = 18, hjust = -3)) +
    theme(plot.subtitle=element_text(color=color.subtitle, size=15, vjust=1.25)) +
    theme(axis.text.x=element_text(size=base_size * 6,color=color.axis.text)) +
    theme(axis.text.y=element_text(size=base_size * 6,color=color.axis.text)) +
    theme(axis.title.x=element_text(size=base_size * 7,color=color.axis.title, vjust=0)) +
    theme(axis.title.y=element_text(size=base_size * 7,color=color.axis.title, vjust=1.25)) +

    # Plot margins
    theme(plot.margin = grid::unit(c(0.35, 0.2, 0.3, 0.35), "cm")) +
    theme(text=element_text(size=base_size*9)) +
    theme(plot.title=element_text(color=color.title, size=25, vjust=1.25)) +
    
    theme(
      panel.background = element_rect(fill = "transparent", colour = NA),
      plot.background = element_rect(fill = "transparent", colour = NA),
      legend.background = element_rect(fill = "transparent", colour = NA),
      legend.box.background = element_rect(fill = "transparent", colour = NA))
}


p <- ggplot(df, aes(x = platform, y = lifetime_days, color = factor(platform))) +
			geom_jitter(alpha = 0.1) +
			geom_boxplot() +
			labs(y = 'Lifetime Days') +
			theme_periscope(base_size = 2.3) +
			# Add Periscope colors
			scale_color_manual(values = c("#947CB0", "#663399", "#AEA8D3", "#9A12B3","#BE90D4", "#9B59B6", "#DCC6E0", "#674172", "#913D88"))

periscope.image(p)
