import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    THE_COMMANDS = ["line", "scale", "move", "rotate", "save", "circle", "bezier", "hermite", "box", "sphere", "torus"]
    
    p = mdl.parseFile(filename)

    systems = [tmp]
    step = 0.1
    
    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = []
    step = 0.1

    
    for command in commands:
        line = command[0]
        edges = stack[0]

        if command[0] in THE_COMMANDS:
            args = command[1:]


            #SPHERE
            if line == 'sphere':
                add_sphere(edges,
                           float(args[0]),
                           float(args[1]),
                           float(args[2]),
                           float(args[3]),
                           step
                )
                matrix_mult( systems[-1], edges)
                draw_polygons(edges, screen, color)
                edges = []

                
            #TORUS 
            elif line == 'torus':
                add_torus(edges,
                          float(args[0]),
                          float(args[1]),
                          float(args[2]),
                          float(args[3]),
                          float(args[4]),
                          step
                )
                matrix_mult( systems[-1], edges)
                draw_polygons(edges, screen, color)
                edges = []


            #BOX
            elif line == "box":
                add_box(edges,
                        float(args[0]),
                        float(args[1]),
                        float(args[2]),
                        float(args[3]),
                        float(args[4]),
                        float(args[5])
                        )
                matrix_mult(systems[-1], edges)
                draw_polygons(edges, screen, color)
                edges = []


            #CIRCLE    
            elif line == "circle":
                add_cicle(edges,
                          float(args[0]),
                          float(args[1]),
                          float(args[2]),
                          float(args[3]),
                          step
                          )


            #CURVES    
            elif line == "hermite" or line == "bezier":
                add_curve(edges,
                          float(args[0]),
                          float(args[1]),
                          float(args[2]),
                          float(args[3]),
                          float(args[4]),
                          float(args[5]),
                          float(args[6]),
                          float(args[7]),
                          step,
                          line
                          )


            #LINE
            elif line == "line":
                add_edge(edges,
                         float(args[0]),
                         float(args[1]),
                         float(args[2]),
                         float(args[3]),
                         float(args[4]),
                         float(args[5])
                         )



            #SCALE
            elif line == "scale":
                t = make_scale(float(args[0]),
                               float(args[1]),
                               float(args[2])
                               )
                matrix_mult(systems[-1], t)
                systems[-1] = [ x[:] for x in t]


            #MOVE
            elif line == "move":
                t = make_translate(float(args[0]),
                                   float(args[1]),
                                   float(args[2])
                                   )
                matrix_mult(systems[-1], t)
                systems[-1] = [x[:] for x in t]


            #ROTATE
            elif line == "rotate":
                theta = float(args[1]) * (math.pi / 180)

                if args[0] == "x":
                    t = make_rotX(theta)
                elif args[0] == "y":
                    t = make_rotY(theta)
                else:
                    t = make_rotZ(theta)
                    matrix_mult(systems[-1:], t)
                    systems[-1] = [ x[:] for x in t]


            #CLEAR
            elif line == "clear":
                edges = []

            #IDENT
            elif line == "ident":
                ident(transform)

            #APPLY
            elif line == "apply":
                matrix_mult(transform, edges)

            #PUSH
            elif line == "push":
                systems.append( [ x[:] for x in systems[-1]])

            #POP
            elif line == "pop":
                systems.pop()

            #DISPLAY
            elif line == "display": 
                display(screen)

            #SAVE
            elif line == "save":
                save_extension(screen, args[0])

        
        print command
