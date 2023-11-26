vertex_shader = """
    #version 330
    in vec4 position;
    out float height;

    uniform mat4 modelviewprojection;

    void main()
    {
        gl_Position = modelviewprojection * position;
        height = position.z;
    }
    """
fragment_shader = """
#version 330
in float height;
out vec4 FragColor;

void main()
{
    vec3 color = mix(vec3(1.0, 1.0, 1.0), vec3(0.0, 1.0, 0.0), height);
    color = mix(color, vec3(1.0, 1.0, 0.0), height);
    color = mix(color, vec3(.0, 1.0, 0.0), height);
    
    FragColor = vec4(color, 1.0);
}
"""