import os

os.chdir('app/jurisdiction')

with open('mapper.py', 'r') as f:
    content = f.read()

method = '''

    def get_required_controls(self, jurisdiction: str, action_context: Dict) -> Tuple[List[str], float]:
        """
        Phase 110, Task 4: Get required controls for a jurisdiction and action.
        Wraps assess_action with extended functionality for PolicyEngine integration.
        """
        # Delegate to assess_action for core logic
        controls, score = self.assess_action(jurisdiction, action_context)
        
        # Extended logic for additional context parameters
        rule = self.loader.get_jurisdiction_rules(jurisdiction)
        
        if rule and rule.active:
            mappings = rule.control_mappings
            
            # Check for cross-border transfer requirements
            if action_context.get('cross_border_transfer'):
                if 'cross_border_transfer' in mappings:
                    controls.append(mappings['cross_border_transfer'])
                elif jurisdiction in ['EU', 'UK', 'BR-LGPD']:
                    controls.append('CROSS_BORDER_TRANSFER_AUTH')
        
        # Deduplicate and return
        controls = list(dict.fromkeys(controls))
        return controls, max(0.0, score)
'''

with open('mapper.py', 'w') as f:
    f.write(content + method)

print('Method added successfully')