from OpenGL.GL import *

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise Exception("Shader compilation failed: {}".format(glGetShaderInfoLog(shader)))

    return shader

def link_program(vertex_shader, fragment_shader):
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise Exception("Program linking failed: {}".format(glGetProgramInfoLog(program)))

    return program

def init_shader_program(vertex_shader, fragment_shader):
    vertex_shader_obj = compile_shader(vertex_shader, GL_VERTEX_SHADER)
    fragment_shader_obj = compile_shader(fragment_shader, GL_FRAGMENT_SHADER)
    shader_program =  link_program(vertex_shader_obj, fragment_shader_obj)
    glDeleteShader(vertex_shader_obj)
    glDeleteShader(fragment_shader_obj)
    return shader_program