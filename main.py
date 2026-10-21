import bpy
import os

# === LIMPAR A CENA ===
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# === CONFIGURAÇÕES ===
ASSETS_DIR = r"C:\\Users\\glauc\\OneDrive\\Desktop\\SI - CEST\\2026.2 - 6p\\Computação Gráfica\\solar-system\\assets"
bpy.context.scene.render.engine = 'CYCLES'


def criar_corpo(nome, arquivo, posicao, escala):
    """Cria uma esfera com a textura de imagem aplicada."""
    img_path = os.path.join(ASSETS_DIR, arquivo)

    # Cria esfera
    bpy.ops.mesh.primitive_uv_sphere_add(location=posicao)
    obj = bpy.context.object
    obj.name = nome
    obj.scale = (escala, escala, escala)
    bpy.ops.object.shade_smooth()

    # Cria material com nodes
    mat = bpy.data.materials.new(name=f"Mat_{nome}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Remove nós extras e mantém o principal
    for n in list(nodes):
        if n.name not in ("Material Output", "Principled BSDF"):
            nodes.remove(n)
    bsdf = nodes["Principled BSDF"]

    # Nó de textura de imagem
    tex_node = nodes.new(type="ShaderNodeTexImage")
    try:
        tex_node.image = bpy.data.images.load(img_path)
    except RuntimeError as e:
        print(f"[ERRO] Não foi possível carregar a textura de {nome}: {img_path}\n{e}")

    # Liga a textura ao BSDF
    links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])

    # Aplica o material
    obj.data.materials.append(mat)
    print(f"{nome} criado.")
    return obj


# === CORPOS CELESTES ===
# (nome, arquivo da textura, posição (x, y, z), escala)
corpos = [
    ("Sol",      "sun-texture.jpg",      (0,   0, 15), 10),
    ("Mercurio", "mercurio-texture.avif", (20,  0, 15), 2),
    ("Venus",    "venus-texture.jpg",    (30,  0, 15), 3),
    ("Terra",    "terra-texture.jpg",    (42,  0, 15), 3),
    ("Marte",    "marte-texture.avif",    (54,  0, 15), 2.5),
    ("Jupiter",  "jupiter-texture.jpg",  (72,  0, 15), 7),
    ("Saturno",  "saturno-texture.jpg",  (92,  0, 15), 6),   # anel: depois
    ("Urano",    "urano-texture.jpg",    (110, 0, 15), 4),   # anel: depois
    ("Netuno",   "netuno-texture.jpg",   (126, 0, 15), 4),
]

for nome, arquivo, pos, escala in corpos:
    criar_corpo(nome, arquivo, pos, escala)


# === AJUSTAR VISUALIZAÇÃO PARA MATERIAL PREVIEW ===
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'
                space.shading.use_scene_lights = True
                space.shading.use_scene_world = True
                print("Viewport alterado para MATERIAL PREVIEW")

print("Sistema solar criado com sucesso.")