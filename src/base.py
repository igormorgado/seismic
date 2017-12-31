#!/usr/bin/env python
"""
This code implements all algorithms described on
SILVA2015 - Introducao ao metodo sismico: Modelagem Computacional

Serao utilizadas a principio as mesmas variaves e nomeclaturas usadas
no artigo
"""

import numpy as np

# pylint: disable=locally-disabled, invalid-name

def wavelength(initial_position, final_position):
    """Retorna 'lambda' (comprimento de onda), dados dois picos r1, r0.

    Args:
        initial_position (float): Inicio do Intervalo.
        final_position (float): Final do intervalo.

    Returns:
        float: Comprimento de onda (lambda)
    """

    return final_position - initial_position


def period(initial_time, final_time):
    """Retorna o periodo do intervalo.

    Args:
        initial_time (float): Inicio do intervalo.
        final_time (float): Fim do intervalo.

    Returns:
        float: Tamanho do intervalo.
    """

    return initial_time - final_time


def wave_velocity(initial_position, initial_time, final_position, final_time):
    """Retorna a velocidade da onda como a razao entre duas cristas de onda.

    Args:
        initial_position (float): Inicio do Intervalo.
        initial_time (float): Inicio do intervalo.
        final_position (float): Final do intervalo.
        final_time (float): Fim do intervalo.

    Returns:
        float: Velocidade da onda
    """
    return (wavelength(initial_position, final_position) /
            period(initial_time, final_time))


def frequency(initial_time, end_time):
    """Retorna a frequencia baseado no intervalo de tempo.

    Args:
        t0 (float): Inicio do intervalo.
        t1 (float): Fim do intervalo.

    Return:
        float: Frequencia.
    """
    return 1/period(initial_time, end_time)


def velocity_p_by_distance(x, t):
    """Retorna a velocidade da onda compressional dados distancia e tempo

    Args:
        x (float): Distancia percorrida.
        t (float): Tempo percorrido.

    Returns:
        float: velocidade compressional
    """
    return x/t


def velocity_p_by_shear(rho, mu, k):
    """Retorna a velocidade da onda P (compressional) pelas propriedades da
    rocha.

    Args:
        rho (float): Densidade do material.
        mu (float): Modulo de cisalhamento (mede deformacao sem mudanca de
        volume).
        k (float): Modulo da deformacao volumetrica (Bulk).

    Returns:
        float: velocidade compressional.
    """
    return np.sqrt((k + (4/3) * mu) / rho)


def velocity_p_by_young(rho, E, sigma):
    """Retorna a velocidade da onda P (compressional) pelas propriedades da
    rocha.

    Args:
        rho (float): densidade do material.
        E (float): Modulo de Young (proporcionalidade entre a tensao e a
        deformacao).
        sigma (float): Coeficiente de Poisson (razao da contracao transversal
        e extensao longitudinal.

    Returns:
        float: Velocidade compressional.
    """
    return np.sqrt((E/rho) * (1-sigma) / ((1-2*sigma)*(1 + sigma)))


def Vp(density=None, young=None, poisson=None,
       shear=None, deformation=None, distance=None, time=None):
    """Retorna a velocidade da onda compressional (P) pelas propriedades dadas.

    Para computacao, deve se entrar uma das seguintes combinacoes de
    parametros:
    * density, young, poisson;
    * density, shear, deformation;
    * distance, time

    Args:
        density (float): Densidade do material (rho).
        young (float): Coeficiente de Young (E).
        poisson (float): Coeficiente de poisson (sigma)
        shear (float): Coeficiente compressional (mu)
        deformation (float): Deformacao do material (k) (Bulk's)
        distance (float): Distancia em metros (x)
        time (float): tempo percorrido (t).

    Returns:
        float: Velocidade da onda P.
    """
    if density is not None and density > 0:
        if young is not None and young > 0 and poisson is not None and poisson > 0:
            return velocity_p_by_young(density, young, poisson)
        elif (shear is not None and shear > 0 and
              deformation is not None and deformation > 0):
            return velocity_p_by_shear(density, shear, deformation)
    elif distance is not None and time is not None and time > 0:
        return velocity_p_by_distance(distance, time)
    else:
        raise ValueError("You should supply positives 'density, shear, deformation' "
                         "or 'density, young, poisson' or 'distance,time' where "
                         "0 < poisson < .5'")


def velocity_s_by_shear(rho, mu):
    """ Retorna a velocidade da onda S (cisalhante) dados mu e rho.

    Args:
        rho (float): Coeficiente de Cisalhamento
        mu (float): Coeficiente de densidade.

    Returns:
        float: Velocidade cisalhante
    """
    return np.sqrt(mu/rho)


def velocity_s_by_young(rho, E, sigma):
    """ Retorna a velocidade da onda S dados sigma e rho.

    Args:
        rho (float): Coeficiente de densidade (rho)
        E (float): Young's soefficient
        sigma (float): Coeficiente de Poisson (sigma)

    Returns:
        float: Velocidade cisalhante
    """
    return np.sqrt(E / (2 * rho * (1 + sigma)))


def Vs(density, shear=None, young=None, poisson=None):
    r"""Returns shear velocity based on physical coefficients.

    You should supply one of the two parameter combinations:

    * density and shear;

    * density, Young and Poisson coefficient

    This function verifies the values, therefore is slower, if you need faster
    function, call directly:

    * velocity_s_by_shear

    * velocity_s_by_young

    Args:
        density (float): Density (non negative) ( :math:`\rho` ).
        shear (float): Shear (non negative) ( :math:`\mu` ).
        young (float): Young coefficient (E).
        poisson (float): Poisson coefficient. :math:`0 < \sigma < 1/2` .

    Returns:
        float: Shear velocity
    """
    if density <= 0:
        raise ValueError("Density must be a positive value")

    if shear is not None and shear > 0:
        return velocity_s_by_shear(density, shear)
    elif (young is not None   and young > 0 and
          poisson is not None and (0 < poisson < .5)):
        return velocity_s_by_young(density, young, poisson)
    else:
        raise ValueError("You should supply positives 'density and shear'"
                         "or 'density, young, poisson', where 0 < poisson < .5'")


def velocity_ratio_by_deformation(k, mu):
    """Retorna a razao entre a velocidade P e S.

    Args:
        deformation (float): Coeficiente de deformacao (de Bulk)
        shear (float): Coeficiente de cisalhamento

    Returns:
        float: Razao da velocidade Vp/Vs.
    """
    return np.sqrt((k/mu) + (4/3))


def velocity_ratio_by_poisson(sigma):
    """Retorna a razao entre a Vp e Vs

    Args:
        poisson (float): Coeficiente de poisson

    Returns:
        float: Razao da velocidade Vp/Vs
    """
    return np.sqrt((1-sigma)/(0.5-sigma))


def velocity_ratio(deformation=None, shear=None, poisson=None):
    """Returns velocity ratio P/S

    The function requires "deformation and shear"  OR poisson coefficients. If
    all three are supplied Poisson is ignored.

    This function is slower since it does verifications but safer.  If you
    want to call without value verification use:
    * velocity_ratio_by_deformation
    * velocity_ratio_by_poisson

    Args:
        deformation (float): Deformation factor (k), must be positive.
        shear (float): Shear factor (mu), must be positive.
        poisson (float): Poisson coeficient (sigma),  0 < sigma < 1/2.

    Returns:
        float: Velocity ratio P/S. Always a number bigger than 1.
    """
    if deformation is not None and deformation > 0 and shear is not None and shear > 0:
        return velocity_ratio_by_deformation(deformation, shear)
    elif poisson is not None and (0 < poisson < .5):
        return velocity_ratio_by_poisson(poisson)
    else:
        raise ValueError("You should supply positives 'deformation and shear'"
                         " or a 'poisson' coefficient in (0,1/2)")


def acoustic_impedance(density, velocity):
    """Returns acoustic impedance

    Args:
        density (float): Density (rho).
        velocity (float): Wave velocity (V)

    Returns:
        float: Acoustic impedance
    """
    return density*velocity


def reflection_coefficient(z1, z2):
    """Returns the reflection coefficient.

    Args:
        z1 (float): Acoustic impedance of upper layer.
        z2 (float): Acoustic impedance of lower layer.

    Returns:
        float: Reflection coefficient.
    """
    return (z2 - z1)/(z2 + z1)
