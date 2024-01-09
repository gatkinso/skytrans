# skytrans

Shared Skywire message transport.


brew install autoconf automake libtool shtool

https://github.com/grpc/grpc  v1.40.0
https://github.com/google/googletest

python3 -m venv pytrans
pip install grpcio  
pip install grpcio-tools


export NEO4J_USERNAME=neo4j ; export NEO4J_BOLT_URL=bolt://neo4j:password@localhost:7687 ; export NEO4J_PASSWORD=password ; export PYTHONPATH=~/apps/skytrans/bin/pytrans/

export PATH="$PATH:$(go env GOPATH)/bin"

cmake -S skytrans -B build_skytrans/ -D CMAKE_INSTALL_PREFIX=$HOME/apps/skytrans -D CMAKE_PREFIX_PATH="~/apps/EZ/grpc;~/apps/EZ/protobuf;~/apps/EZ/googletest"

cmake --build build_st/ --target install