---
title: Create 3D Icon
emoji: 🎨
colorFrom: purple
colorTo: gray
sdk: docker
app_port: 7860
---

# Create 3D Icon

This is a small cli tool to generate 3D icons using Blender.

> I use this side project to learn Blender with Python.

## Examples

```bash
python create.py examples/LogosGithubIcon.svg
```

|                         from                         |                           to                            |
| :--------------------------------------------------: | :-----------------------------------------------------: |
| ![LogosGithubIcon.svg](examples/LogosGithubIcon.svg) | ![LogosGithubIcon.png](https://i.imgur.com/Lgt0UNO.png) |

---

```bash
python create.py --light-x 1 --light-strength 2 examples/LogosBlender.svg
```

|                      from                      |                          to                          |
| :--------------------------------------------: | :--------------------------------------------------: |
| ![LogosBlender.svg](examples/LogosBlender.svg) | ![LogosBlender.png](https://i.imgur.com/GuUWMc6.png) |

---

```bash
python create.py -r 0 -g 0.1 -b 0.3 -rx 5 -rz 5 -lx 1 -lz -1 -ls 100 --th 2 -d 0.6 examples/LogosGithub.svg
```

|                     from                     |                         to                          |
| :------------------------------------------: | :-------------------------------------------------: |
| ![LogosGithub.svg](examples/LogosGithub.svg) | ![LogosGithub.png](https://i.imgur.com/w4yth2t.png) |

> Icons are from [SVG Logos](https://github.com/gilbarbara/logos) (CC0)

## Install

I use poetry to manage dependencies.

```bash
poetry env use 3.10
poetry install
```

You may need to install [Blender](https://www.blender.org/download/) and add it to your path.
