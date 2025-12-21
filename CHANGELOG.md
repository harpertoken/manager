# Changelog

## [0.3.1](https://github.com/bniladridas/manager/compare/manager-v0.3.0...manager-v0.3.1) (2025-12-21)


### Bug Fixes

* add remote repo name to cla action ([4277a25](https://github.com/bniladridas/manager/commit/4277a25231caa3e8c265d18b4f3a538f4ba72ccc))
* remove allowlist from cla action ([33ec3bb](https://github.com/bniladridas/manager/commit/33ec3bbdd6055777eb253b26ffcafbfef11ac774))
* remove duplicate test function ([9b1b693](https://github.com/bniladridas/manager/commit/9b1b6930922a3e67cec9f1ff733aa1b932e5157a))
* remove duplicate test function ([395e4b3](https://github.com/bniladridas/manager/commit/395e4b3cc9b03cf044defe1c7e1c7e881db21266))
* remove redundant test ([5955d7a](https://github.com/bniladridas/manager/commit/5955d7a7b58a8f9aed28bd0650e97fc4b4d15473))
* set allowlist to empty string ([d192f51](https://github.com/bniladridas/manager/commit/d192f513234845b7566296dc81f133524079e172))
* update cla action to v2.6.2 ([b3c81de](https://github.com/bniladridas/manager/commit/b3c81deb6e57e37f1b4cc4ea2c6d1ce3b99db38e))
* use local path for cla document ([81deb33](https://github.com/bniladridas/manager/commit/81deb33b75d9c175e83c350faa721b139701193a))


### Documentation

* update CLA template for manual signing ([#18](https://github.com/bniladridas/manager/issues/18)) ([2d1eb25](https://github.com/bniladridas/manager/commit/2d1eb2501c0e680d423c2e5879c2d1e774513da9))

## [0.3.0](https://github.com/bniladridas/manager/compare/manager-v0.2.0...manager-v0.3.0) (2025-12-10)


### Features

* cla system and signatures ([#11](https://github.com/bniladridas/manager/issues/11)) ([0ab89a1](https://github.com/bniladridas/manager/commit/0ab89a1d88fd502791c74122acab011757ac78eb))


### Bug Fixes

* add sha to checks action ([e7b6c14](https://github.com/bniladridas/manager/commit/e7b6c14edb1679a547ab993a9fc6a07b916e0746))
* **cla:** add checks write permission for status updates ([47ebd1c](https://github.com/bniladridas/manager/commit/47ebd1c99ba60d4e20df9d32e86a6a5e6d825918))
* correct yaml indentation ([54fb953](https://github.com/bniladridas/manager/commit/54fb953988b90d2bcfbad2d9dfd1e7ba51a51b19))
* init cla.json as object ([b85d90b](https://github.com/bniladridas/manager/commit/b85d90b2c7f0efd6062b08028cad41320ec4d62e))
* store cla signatures locally ([6e12e97](https://github.com/bniladridas/manager/commit/6e12e974662713eb610d2a25c68955e3b328cbed))


### Chores

* update release-please action ([bfca2e3](https://github.com/bniladridas/manager/commit/bfca2e36cf4aa360674ed8bb44d5d5ea1118c1df))

## [0.2.0](https://github.com/bniladridas/manager/compare/manager-v0.1.0...manager-v0.2.0) (2025-12-09)


### Features

* add initial project structure ([eae46a3](https://github.com/bniladridas/manager/commit/eae46a3dc436d43d0c40ca40b3aa1eb8a2b605f6))
* add templates and cli improvements ([7b5c29c](https://github.com/bniladridas/manager/commit/7b5c29cf92c06a78c5f19cc2ebe4df54007973b2))
* typing, tests, docs ([fb3d7bf](https://github.com/bniladridas/manager/commit/fb3d7bf3faa9990b54ca9fbec712f8bfcef0e9e2))


### Bug Fixes

* add missing path import ([d495c98](https://github.com/bniladridas/manager/commit/d495c9808f9ea0548938f0df9d292793a075b544))
* correct advanced.jinja template ([580f79c](https://github.com/bniladridas/manager/commit/580f79ca591df3debd1cae2e5f0a06004d157a56))
* correct cla section reference ([cee5ab5](https://github.com/bniladridas/manager/commit/cee5ab5f8fb7c4e38d0a7e737913d57ce6b84d7b))
* exclude signatures from packages ([f1e7bda](https://github.com/bniladridas/manager/commit/f1e7bda58c0972635f6a1d1feaf81ab97a0e7dc2))
* move checkout from composite action ([cc0500f](https://github.com/bniladridas/manager/commit/cc0500f8a5fb64131dcd08a3170b604991bf5e37))
* move jinja2 import inside __init__ ([b7f2b44](https://github.com/bniladridas/manager/commit/b7f2b44c4f74124dc1899d825b5d9f5bb2f3c6f9))
* optional message for setup-hooks ([b877cdb](https://github.com/bniladridas/manager/commit/b877cdb9916998f5462a6124970b100dba880a2b))
* remove duplicate support section ([9fd90a8](https://github.com/bniladridas/manager/commit/9fd90a8b81cb0dc03a9d6179ecb57b90990fa645))
* remove hardcoded cwd from tests ([64a7495](https://github.com/bniladridas/manager/commit/64a74951814fe91858f197dbad0cf6c88f24f149))
* remove python 3.8 from ci matrix ([ac2dd47](https://github.com/bniladridas/manager/commit/ac2dd476e7ccf18ad0bc32caad5aa18190218763))
* set signatures branch to head_ref ([3ee21d9](https://github.com/bniladridas/manager/commit/3ee21d972bd179f2e1a8709c53fb0c537d053cc4))
* update cla workflow config ([3ee4c18](https://github.com/bniladridas/manager/commit/3ee4c18cd12703e00d7701f150dde7eb1a6f69e5))
* use generic third-party placeholder ([722d6d1](https://github.com/bniladridas/manager/commit/722d6d1938cd6cfc347c96747a9bcd993d97433b))


### Documentation

* add architecture and schema ([122d8be](https://github.com/bniladridas/manager/commit/122d8be3acf1f914a0ae1c103508b55aa790afa7))
* add contributing guidelines ([b724703](https://github.com/bniladridas/manager/commit/b724703219cee3d7245fb186a31f454f07736512))
* update API reference with type hints ([62cd129](https://github.com/bniladridas/manager/commit/62cd1290d24a39826ac7c7531ca791824d6f4176))


### Styles

* fix end of files ([77078e1](https://github.com/bniladridas/manager/commit/77078e1489cce7117d315e6b25711174932d0bb3))
* move imports to top ([59c740c](https://github.com/bniladridas/manager/commit/59c740cc344d09dbfc30458f233520115cd2868e))


### Code Refactoring

* **path:** migrate from os.path to pathlib ([e1ff0b5](https://github.com/bniladridas/manager/commit/e1ff0b584d9d7bfc7720aeb926145ed12db3cf0b))
* simplify kwargs construction ([5fc109f](https://github.com/bniladridas/manager/commit/5fc109ff2e3a5b6e2b105529e58248914b8e055c))


### Chores

* add workflows and update docs ([51a2c9b](https://github.com/bniladridas/manager/commit/51a2c9b0ff9fb5d4089580718f69c7b24e19b155))
* remove setup.py ([57f8935](https://github.com/bniladridas/manager/commit/57f89355ef0e7979df2f85c562c11001c7bb5354))

## Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
