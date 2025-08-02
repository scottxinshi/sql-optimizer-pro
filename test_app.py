#!/usr/bin/env python3
"""
Test script for SQL Optimizer Pro
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sql_analyzer import SQLAnalyzer
from sql_optimizer import SQLOptimizer

def test_sql_analysis():
    """Test the SQL analysis functionality"""
    print("🧪 Testing SQL Optimizer Pro...")
    
    # Test queries
    test_queries = [
        {
            "name": "Basic SELECT with issues",
            "sql": "SELECT * FROM users WHERE age > 25 ORDER BY name;"
        },
        {
            "name": "Complex JOIN query",
            "sql": """
            SELECT u.name, o.order_date, p.name 
            FROM users u 
            JOIN orders o ON u.id = o.user_id 
            JOIN order_items oi ON o.id = oi.order_id 
            JOIN products p ON oi.product_id = p.id;
            """
        },
        {
            "name": "Query with subquery",
            "sql": """
            SELECT * FROM users 
            WHERE id IN (SELECT user_id FROM orders WHERE total_amount > 1000);
            """
        },
        {
            "name": "Aggregation query",
            "sql": """
            SELECT category_id, COUNT(*) as product_count 
            FROM products 
            GROUP BY category_id;
            """
        },
        {
            "name": "CROSS JOIN example",
            "sql": "SELECT * FROM users CROSS JOIN orders;"
        }
    ]
    
    analyzer = SQLAnalyzer()
    optimizer = SQLOptimizer()
    
    total_tests = len(test_queries)
    passed_tests = 0
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}/{total_tests}: {test['name']}")
        print(f"SQL: {test['sql'].strip()}")
        
        try:
            # Parse and analyze
            parsed_queries = analyzer.parse_sql(test['sql'])
            analysis_results = analyzer.analyze_queries(parsed_queries)
            optimization_suggestions = optimizer.generate_suggestions(analysis_results)
            
            # Display results
            for j, (query, analysis) in enumerate(zip(parsed_queries, analysis_results)):
                print(f"\n  Query {j+1} Analysis:")
                print(f"  - Type: {analysis['query_type']}")
                print(f"  - Tables: {', '.join(analysis['tables'])}")
                print(f"  - Performance: {analysis['estimated_performance']}")
                print(f"  - Complexity Score: {analysis['complexity_score']}")
                print(f"  - Issues Found: {len(analysis['issues'])}")
                
                if analysis['issues']:
                    print("  - Issues:")
                    for issue in analysis['issues']:
                        print(f"    • {issue['severity'].upper()}: {issue['message']}")
                
                if optimization_suggestions[j]:
                    print(f"  - Suggestions: {len(optimization_suggestions[j])}")
                    for suggestion in optimization_suggestions[j][:2]:  # Show first 2 suggestions
                        print(f"    • {suggestion['title']}")
            
            # Calculate overall score
            score = optimizer.calculate_optimization_score(analysis_results)
            print(f"  - Overall Score: {score:.1f}/100")
            
            passed_tests += 1
            print("  ✅ Test passed")
            
        except Exception as e:
            print(f"  ❌ Test failed: {str(e)}")
    
    print(f"\n🎉 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🚀 All tests passed! SQL Optimizer Pro is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

def test_api_endpoint():
    """Test the API endpoint functionality"""
    print("\n🌐 Testing API endpoint...")
    
    try:
        import requests
        import json
        
        # Test data
        test_data = {
            "sql": "SELECT * FROM users WHERE age > 25;"
        }
        
        # Make API request
        response = requests.post(
            "http://localhost:5000/api/analyze",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API endpoint is working")
            print(f"   - Analysis results: {len(result.get('analysis', []))} queries analyzed")
            print(f"   - Optimization score: {result.get('optimization_score', 0):.1f}/100")
            return True
        else:
            print(f"❌ API endpoint failed with status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API endpoint. Make sure the server is running.")
        return False
    except Exception as e:
        print(f"❌ API test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 SQL Optimizer Pro - Test Suite")
    print("=" * 60)
    
    # Test core functionality
    core_tests_passed = test_sql_analysis()
    
    # Test API endpoint (if server is running)
    api_tests_passed = test_api_endpoint()
    
    print("\n" + "=" * 60)
    print("📊 Final Test Summary:")
    print(f"   Core Functionality: {'✅ PASSED' if core_tests_passed else '❌ FAILED'}")
    print(f"   API Endpoint: {'✅ PASSED' if api_tests_passed else '❌ FAILED'}")
    
    if core_tests_passed:
        print("\n🎉 SQL Optimizer Pro is ready to use!")
        print("💡 To start the web server, run: python app.py")
        print("🌐 Then open your browser to: http://localhost:5000")
    else:
        print("\n⚠️  Please fix the failing tests before using the application.")
    
    print("=" * 60) 