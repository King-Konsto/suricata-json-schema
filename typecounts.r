library(ggplot2)
library(reshape)
library(RColorBrewer)
library(colorspace)

counts <- read.csv("typecounts.csv")
mdata=melt(counts,id=c("version"))

baseCols =c("#002C4E", "#0074A1", "#71AB1A", "#B8DB64", "#A2B2BE",
            "#CBE0AB", "#BDC4CD", "#E5F1C6", "#1F2F08", "#00202C",
            "#45657E", "#97C158", "#CBE48E", "#7C899C")
cols = replicate(10,sample(baseCols,length(baseCols),replace = TRUE))
  
ggplot(mdata, aes(x=version,y=value,group=variable,fill=variable)) +
  geom_area(aes(fill=variable)) +
  scale_fill_manual(values=cols) +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 60, hjust = 1)) + 
  theme(legend.title = element_blank()) +
  labs(x = "Suricata version", y = "count", legend = NULL)

ggsave(file="typecounts.pdf", width=10, height=4.6, dpi=300)
