def generate():
    """switchs ARM to Thumb mode

    """
    sc = """
    .arm
    add r6, pc, #1
    bx
    .thumb
    """
    return sc
