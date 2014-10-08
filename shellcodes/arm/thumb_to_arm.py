def generate():
    """switchs Thumb to ARM mode

    """
    sc = """
    .thumb 
    .align 2
    bx pc
    nop
    .arm
    """
    return sc
