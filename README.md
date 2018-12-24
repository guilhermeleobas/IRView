# IRView

![](https://i.imgur.com/wFskAmn.gif)

## What it does

A quickly way to visualize callgraph, control flow graph, regions, ... of LLVM Intermediate Representation files on Sublime Text.

## But *-view-** passes already does that, no?

Yes but those passes never worked with me. 

## Which passes are supported by IRView?

- callgraph
- cfg (-only)
- dom (-only)
- postdom (-only)
- regions (-only)

## Dependencies

Make sure you have `dot` in your path. `dot` can be obtained by installing the graphviz package. Check their [website](https://graphviz.gitlab.io/download/) for more info.

## Contributing

Please, test it on other platforms (Linux and Windows).

## Found a bug?

Please, report