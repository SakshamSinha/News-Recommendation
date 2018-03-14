# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase
from retrieval.data_retrieval import NewsRetrieval
# Create your tests here.


class TestDataRetrieval(TestCase):
    """Test the access key."""

    def test_newsapi(self):
        """Check the connectivity using the newsapi key."""
        dataRetrieval = NewsRetrieval()
        self.assertTrue(dataRetrieval.check_connectivity_using_key())