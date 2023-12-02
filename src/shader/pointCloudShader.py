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
    vec3 brownColor = vec3(43.0/255.0, 63.0/255.0, 0.0/255.0);
    
    vec3 greenColor = vec3(34.0/255.0, 139.0/255.0, 34.0/255.0);

    vec3 color = mix(brownColor, greenColor, height);

    FragColor = vec4(color, 1.0);
}
"""