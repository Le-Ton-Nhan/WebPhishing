


def combine(static_pre, static_score, dynamic_pre, dynamic_score):
    label = ""
    final_score = 0

    static_pre = float(static_pre/100)
    static_score = float(static_score)
    dynamic_pre = float(dynamic_pre)
    dynamic_score = float(dynamic_score)
    if static_pre == dynamic_pre:
        final_score = static_score*0.3 + dynamic_score*0.7
        if final_score >= 0.8:
            if static_pre == 1:
                label = "phishing"
            else:
                label = "normal"
        else:
            label = "warning"

    else:
        label = "warning"
    
    return label, final_score
