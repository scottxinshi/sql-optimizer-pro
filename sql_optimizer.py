from typing import List, Dict, Any
import re

class SQLOptimizer:
    def __init__(self):
        self.optimization_rules = {
            'index_optimization': self._suggest_index_optimizations,
            'join_optimization': self._suggest_join_optimizations,
            'where_optimization': self._suggest_where_optimizations,
            'select_optimization': self._suggest_select_optimizations,
            'aggregation_optimization': self._suggest_aggregation_optimizations,
            'subquery_optimization': self._suggest_subquery_optimizations,
            'general_optimization': self._suggest_general_optimizations
        }
    
    def generate_suggestions(self, analysis_results: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """Generate optimization suggestions for each query"""
        suggestions = []
        
        for analysis in analysis_results:
            query_suggestions = []
            
            # Apply each optimization rule
            for rule_name, rule_func in self.optimization_rules.items():
                rule_suggestions = rule_func(analysis)
                query_suggestions.extend(rule_suggestions)
            
            # Sort suggestions by priority
            query_suggestions.sort(key=lambda x: self._get_priority_score(x['priority']), reverse=True)
            
            suggestions.append(query_suggestions)
        
        return suggestions
    
    def calculate_optimization_score(self, analysis_results: List[Dict[str, Any]]) -> float:
        """Calculate an overall optimization score (0-100)"""
        if not analysis_results:
            return 100.0
        
        total_score = 0
        max_possible_score = 0
        
        for analysis in analysis_results:
            # Base score based on performance estimation
            performance_scores = {
                'excellent': 100,
                'good': 80,
                'fair': 60,
                'poor': 30,
                'unknown': 50
            }
            
            base_score = performance_scores.get(analysis['estimated_performance'], 50)
            
            # Deduct points for issues
            issue_penalties = {
                'high': 20,
                'medium': 10,
                'low': 5
            }
            
            for issue in analysis.get('issues', []):
                base_score -= issue_penalties.get(issue['severity'], 5)
            
            # Ensure score doesn't go below 0
            base_score = max(0, base_score)
            
            total_score += base_score
            max_possible_score += 100
        
        return (total_score / max_possible_score) * 100 if max_possible_score > 0 else 100
    
    def _suggest_index_optimizations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest index-related optimizations"""
        suggestions = []
        
        # Suggest indexes for WHERE clause columns
        if analysis['where_clause']['has_where']:
            suggestions.append({
                'type': 'index_suggestion',
                'priority': 'high',
                'title': 'Consider adding indexes for WHERE clause columns',
                'description': 'Indexes on columns used in WHERE clauses can significantly improve query performance',
                'code_example': 'CREATE INDEX idx_column_name ON table_name(column_name);',
                'impact': 'High performance improvement for filtering operations'
            })
        
        # Suggest indexes for JOIN columns
        if analysis['joins']['join_count'] > 0:
            suggestions.append({
                'type': 'index_suggestion',
                'priority': 'high',
                'title': 'Add indexes on JOIN columns',
                'description': 'Indexes on columns used in JOIN conditions improve join performance',
                'code_example': 'CREATE INDEX idx_join_column ON table_name(join_column);',
                'impact': 'Significant improvement in join operations'
            })
        
        # Suggest indexes for ORDER BY columns
        if analysis['order_by']['has_order_by']:
            suggestions.append({
                'type': 'index_suggestion',
                'priority': 'medium',
                'title': 'Consider index for ORDER BY columns',
                'description': 'Indexes on ORDER BY columns can eliminate the need for sorting',
                'code_example': 'CREATE INDEX idx_order_column ON table_name(order_column);',
                'impact': 'Eliminates sorting overhead for ORDER BY operations'
            })
        
        return suggestions
    
    def _suggest_join_optimizations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest join-related optimizations"""
        suggestions = []
        
        # Cross join optimization
        if analysis['joins']['cross_joins']:
            suggestions.append({
                'type': 'join_optimization',
                'priority': 'high',
                'title': 'Replace CROSS JOIN with explicit JOIN conditions',
                'description': 'CROSS JOINs can cause performance issues due to Cartesian products',
                'code_example': '-- Instead of: SELECT * FROM table1 CROSS JOIN table2\n-- Use: SELECT * FROM table1 JOIN table2 ON table1.id = table2.id',
                'impact': 'Prevents exponential growth in result sets'
            })
        
        # Multiple joins optimization
        if analysis['joins']['join_count'] > 3:
            suggestions.append({
                'type': 'join_optimization',
                'priority': 'medium',
                'title': 'Consider breaking down complex joins',
                'description': 'Multiple joins can be optimized by using temporary tables or views',
                'code_example': '-- Consider using CTEs or temporary tables for complex join chains',
                'impact': 'Improves readability and potentially performance'
            })
        
        return suggestions
    
    def _suggest_where_optimizations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest WHERE clause optimizations"""
        suggestions = []
        
        # Functions in WHERE clause
        if analysis['where_clause']['functions_used']:
            suggestions.append({
                'type': 'where_optimization',
                'priority': 'medium',
                'title': 'Avoid functions in WHERE clause',
                'description': f"Functions {', '.join(analysis['where_clause']['functions_used'])} in WHERE clause may prevent index usage",
                'code_example': '-- Instead of: WHERE UPPER(column) = \'VALUE\'\n-- Use: WHERE column = \'value\' (if case-insensitive comparison is needed)',
                'impact': 'Enables index usage for better performance'
            })
        
        # OR conditions
        if 'OR conditions may prevent index usage' in analysis['where_clause']['potential_issues']:
            suggestions.append({
                'type': 'where_optimization',
                'priority': 'medium',
                'title': 'Consider UNION instead of OR',
                'description': 'OR conditions can prevent index usage in some cases',
                'code_example': '-- Instead of: WHERE column1 = \'value1\' OR column2 = \'value2\'\n-- Use: SELECT * FROM table WHERE column1 = \'value1\'\n-- UNION\n-- SELECT * FROM table WHERE column2 = \'value2\'',
                'impact': 'May enable better index usage'
            })
        
        return suggestions
    
    def _suggest_select_optimizations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest SELECT clause optimizations"""
        suggestions = []
        
        # Wildcard select
        if '*' in analysis['columns']:
            suggestions.append({
                'type': 'select_optimization',
                'priority': 'medium',
                'title': 'Replace SELECT * with specific columns',
                'description': 'SELECT * retrieves all columns, which may not be necessary',
                'code_example': '-- Instead of: SELECT * FROM table\n-- Use: SELECT column1, column2, column3 FROM table',
                'impact': 'Reduces network transfer and improves performance'
            })
        
        return suggestions
    
    def _suggest_aggregation_optimizations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest aggregation-related optimizations"""
        suggestions = []
        
        # GROUP BY optimization
        if analysis['group_by']['has_group_by']:
            suggestions.append({
                'type': 'aggregation_optimization',
                'priority': 'medium',
                'title': 'Consider index on GROUP BY columns',
                'description': 'Indexes on GROUP BY columns can improve aggregation performance',
                'code_example': 'CREATE INDEX idx_group_column ON table_name(group_column);',
                'impact': 'Improves GROUP BY performance'
            })
        
        return suggestions
    
    def _suggest_subquery_optimizations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest subquery optimizations"""
        suggestions = []
        
        # Subquery optimization
        if analysis['subqueries']:
            suggestions.append({
                'type': 'subquery_optimization',
                'priority': 'medium',
                'title': 'Consider replacing subqueries with JOINs',
                'description': 'Subqueries can sometimes be replaced with more efficient JOINs',
                'code_example': '-- Instead of: SELECT * FROM table1 WHERE id IN (SELECT id FROM table2)\n-- Use: SELECT table1.* FROM table1 JOIN table2 ON table1.id = table2.id',
                'impact': 'Often provides better performance than subqueries'
            })
        
        return suggestions
    
    def _suggest_general_optimizations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest general optimizations"""
        suggestions = []
        
        # Missing LIMIT
        if analysis['query_type'] == 'SELECT' and not analysis['limit']['has_limit']:
            suggestions.append({
                'type': 'general_optimization',
                'priority': 'low',
                'title': 'Add LIMIT clause for large result sets',
                'description': 'Adding LIMIT can prevent memory issues and improve response times',
                'code_example': '-- Add: LIMIT 1000 (or appropriate number)',
                'impact': 'Prevents memory issues with large result sets'
            })
        
        # ORDER BY without LIMIT
        if analysis['order_by']['has_order_by'] and not analysis['limit']['has_limit']:
            suggestions.append({
                'type': 'general_optimization',
                'priority': 'low',
                'title': 'Consider LIMIT with ORDER BY',
                'description': 'ORDER BY without LIMIT may sort entire result set',
                'code_example': '-- Add: LIMIT 1000 after ORDER BY',
                'impact': 'Reduces sorting overhead for large datasets'
            })
        
        # Query complexity
        if analysis['complexity_score'] > 15:
            suggestions.append({
                'type': 'general_optimization',
                'priority': 'medium',
                'title': 'Consider breaking down complex query',
                'description': 'Complex queries can be broken into smaller, more manageable parts',
                'code_example': '-- Use CTEs (Common Table Expressions) or temporary tables',
                'impact': 'Improves maintainability and potentially performance'
            })
        
        return suggestions
    
    def _get_priority_score(self, priority: str) -> int:
        """Convert priority string to numeric score for sorting"""
        priority_scores = {
            'high': 3,
            'medium': 2,
            'low': 1
        }
        return priority_scores.get(priority, 0)
    
    def generate_optimized_query(self, original_query: str, analysis: Dict[str, Any]) -> str:
        """Generate an optimized version of the query"""
        # This is a simplified version - in a real implementation, you'd want more sophisticated query rewriting
        optimized_query = original_query
        
        # Add LIMIT if missing and it's a SELECT query
        if analysis['query_type'] == 'SELECT' and not analysis['limit']['has_limit']:
            if 'ORDER BY' in optimized_query.upper():
                # Add LIMIT after ORDER BY
                optimized_query = re.sub(r'ORDER BY.*$', r'\g<0> LIMIT 1000', optimized_query, flags=re.IGNORECASE)
            else:
                # Add LIMIT at the end
                optimized_query += ' LIMIT 1000'
        
        return optimized_query 