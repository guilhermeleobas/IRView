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

`opt` and `dot`. Make sure you have `dot` in your path. `dot` can be obtained by installing the graphviz package. Check their [website](https://graphviz.gitlab.io/download/) for more info.

If you don't have LLVM installed, check the instructions below on how to download and compile LLVM 6.0

```{bash}
svn co http://llvm.org/svn/llvm-project/llvm/tags/RELEASE_601/final llvm 
cd llvm/tools 
svn co http://llvm.org/svn/llvm-project/cfe/tags/RELEASE_601/final clang 
cd ..
mkdir build
cd build

cmake .. \
-DCMAKE_BUILD_TYPE=Release \
-DLLVM_TARGETS_TO_BUILD="X86" \
-DLLVM_USE_LINKER="gold" \ # options: ld, gold, lld

make -j4
```

## Contributing

Please, test it on other platforms (Linux and Windows).

## Found a bug?

Please, report