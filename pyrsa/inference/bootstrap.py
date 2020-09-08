#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inference module: bootstrapping
"""

import numpy as np
from pyrsa.util.rdm_utils import add_pattern_index


def bootstrap_sample(rdms, rdm_descriptor=None, pattern_descriptor=None):
    """Draws a bootstrap_sample from the data.

    This function generates a bootstrap sample of RDMs resampled over
    measurements and patterns. By default every pattern and RDM sample is
    treated independently. If desired descriptor names can be passed in
    descriptors and in pattern_descriptors to group rdms instead.

    Args:
        rdms(pyrsa.rdm.rdms.RDMs): Data to be used

        rdm_descriptors(String):
            descriptor to group the samples by. For each unique value of
            the descriptor each sample will either contain all RDMs with
            this value or none

        pattern_descriptors(string):
            descriptor to group the patterns by. Each group of patterns will
            be in or out of the sample as a whole

    Returns:
        pyrsa.rdm.rdms.RDMs: rdms
            subsampled dataset with equal number of groups in both patterns
            and measurements of the rdms

        numpy.ndarray: rdm_sample
            sampled rdm indices

        numpy.ndarray: pattern_sample
            sampled pattern descriptor indices

    """
    if rdm_descriptor is None:
        rdm_select = np.arange(rdms.n_rdm)
        rdms.rdm_descriptors['index'] = rdm_select
        rdm_descriptor = 'index'
    else:
        rdm_select = np.unique(rdms.rdm_descriptors[rdm_descriptor])
    pattern_descriptor, pattern_select = \
        add_pattern_index(rdms, pattern_descriptor)
    rdm_sample = np.random.randint(0, len(rdm_select) - 1,
                                   size=len(rdm_select))
    rdm_sample = rdm_select[rdm_sample]
    rdms = rdms.subsample(rdm_descriptor, rdm_sample)
    pattern_sample = np.random.randint(0, len(pattern_select) - 1,
                                       size=len(pattern_select))
    pattern_sample = pattern_select[pattern_sample]
    rdms = rdms.subsample_pattern(pattern_descriptor,
                                  pattern_sample)
    return rdms, rdm_sample, pattern_sample


def bootstrap_sample_rdm(rdms, rdm_descriptor=None):
    """Draws a bootstrap_sample from the data.

    This function generates a bootstrap sample of RDMs resampled over
    measurements. By default every RDM sample is treated independently.
    If desired a descriptor name can be passed inrdm_descriptor to group rdms.

    Args:
        rdms(pyrsa.rdm.rdms.RDMs): Data to be used

        rdm_descriptors(String):
            descriptor to group the samples by. For each unique value of
            the descriptor each sample will either contain all RDMs with
            this value or none

    Returns:
        pyrsa.rdm.rdms.RDMs: rdm_sample
            subsampled dataset with equal number of groups of rdms

        numpy.ndarray: rdm_sample
            sampled rdm indices

        numpy.ndarray: rdm_select
            rdm group descritor values

    """
    if rdm_descriptor is None:
        rdm_select = np.arange(rdms.n_rdm)
        rdms.rdm_descriptors['index'] = rdm_select
        rdm_descriptor = 'index'
    else:
        rdm_select = np.unique(rdms.rdm_descriptors[rdm_descriptor])
    rdm_sample = np.random.randint(0, len(rdm_select) - 1,
                                   size=len(rdm_select))
    rdm_sample = rdm_select[rdm_sample]
    rdms = rdms.subsample(rdm_descriptor, rdm_sample)
    return rdms, rdm_sample


def bootstrap_sample_pattern(rdms, pattern_descriptor=None):
    """Draws a bootstrap_sample from the data.

    This function generates a bootstrap sample of RDMs resampled over
    patterns. By default every pattern is treated independently. If desired
    a descriptor name can be passed in pattern_descriptor to group patterns.

    Args:
        rdms(pyrsa.rdm.rdms.RDMs): Data to be used

        pattern_descriptors(string):
            descriptor to group the patterns by. Each group of patterns will
            be in or out of the sample as a whole

    Returns:
        pyrsa.rdm.rdms.RDMs: rdm_sample
            subsampled dataset with equal number of pattern groups

        numpy.ndarray: pattern_sample
            sampled pattern descriptor index values for subsampling other rdms
    """
    pattern_descriptor, pattern_select = \
        add_pattern_index(rdms, pattern_descriptor)
    pattern_sample = np.random.randint(0, len(pattern_select) - 1,
                                       size=len(pattern_select))
    pattern_sample = pattern_select[pattern_sample]
    rdms = rdms.subsample_pattern(pattern_descriptor,
                                  pattern_sample)
    return rdms, pattern_sample
