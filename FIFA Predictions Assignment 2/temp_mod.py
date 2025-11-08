import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class WorldCupFinalistPredictor:
    def __init__(self, data_file):
        """Initialize the finalist predictor"""
        self.df = pd.read_excel(data_file)
        self.X = None
        self.y = None
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()
        
        
    def create_finalist_target(self):
        """Create target variable for finalist prediction"""
        
        # Since we don't have actual finalist data, we'll create a synthetic target
        # based on elite performance metrics
        conditions = [
            # Elite performance criteria
            (self.df['win_rate'] > 0.65) & (self.df['goal_ratio'] > 1.8) & (self.df['world_cup_experience'] >= 3),
            
            # Historical powerhouses with consistent performance
            (self.df['world_cup_experience'] >= 4) & (self.df['win_rate'] > 0.6) & (self.df['points_per_game'] > 1.8),
            
            # Very dominant teams (high goal ratio)
            (self.df['goal_ratio'] > 2.0) & (self.df['win_rate'] > 0.55)
        ]
        
        choices = [1, 1, 1]  # Mark as potential finalist
        
        self.df['is_finalist'] = np.select(conditions, choices, default=0)
        
        print(f"Created finalist target:")
        
        # Show "finalists"
        finalists = self.df[self.df['is_finalist'] == 1]['Squad'].tolist()
        print(f"   Finalist candidates: {finalists}")
        
        return self.df
    
    def prepare_data(self):
        
        # Select features for modeling
        feature_columns = [
            'win_rate', 'goal_ratio', 'world_cup_experience', 'Appearances',
            'points_per_game', 'goal_diff_per_game', 'MP', 'W', 'Pts', 'GF', 'GA', 'GD'
        ]
        
        # Checking target existance
        if 'is_finalist' not in self.df.columns:
            self.create_finalist_target()
        
        # Remove missing values
        clean_df = self.df[feature_columns + ['is_finalist']].dropna()
        
        self.X = clean_df[feature_columns]
        self.y = clean_df['is_finalist']
        
        # Train Test Split  - stratification because finalists are rare in data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
      
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def build_models(self):
        """Build and train multiple models"""
        print("\n PREDICTION MODELS")
        print("=" * 50)
        
        models = {
            'Logistic Regression': LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000),
            'Random Forest': RandomForestClassifier(class_weight='balanced', random_state=42, n_estimators=100),
            'XGBoost': XGBClassifier(
                scale_pos_weight=len(self.y_train[self.y_train==0])/len(self.y_train[self.y_train==1]), random_state=42, 
                eval_metric='logloss'),
            'Gradient Boosting': GradientBoostingClassifier(random_state=42)
        }
        
        for name, model in models.items():
            print(f"\n {name}...")
            
            try:
                # Use scaled data for Logistic Regression
                if name == 'Logistic Regression':
                    model.fit(self.X_train_scaled, self.y_train)
                    y_pred = model.predict(self.X_test_scaled)
                    y_pred_proba = model.predict_proba(self.X_test_scaled)[:, 1]
                else:
                    model.fit(self.X_train, self.y_train)
                    y_pred = model.predict(self.X_test)
                    y_pred_proba = model.predict_proba(self.X_test)[:, 1]
                
                # Calculate metrics
                accuracy = accuracy_score(self.y_test, y_pred)
                auc_roc = roc_auc_score(self.y_test, y_pred_proba)
                
                self.models[name] = model
                self.results[name] = {
                    'accuracy': accuracy,
                    'auc_roc': auc_roc,
                    'predictions': y_pred,
                    'probabilities': y_pred_proba,
                    'model': model
                }
                
                print(f" Accuracy: {accuracy:.3f}")
                print(f" AUC-ROC: {auc_roc:.3f}")
                
            except Exception as e:
                print(f"Error training {name}: {e}")
        
        return self.models
    
    def evaluate_models(self):
        """Evaluate all models"""
        print("\n MODEL EVALUATION")
        print("=" * 50)
        
        comparison = []
        
        for name, metrics in self.results.items():
            y_pred = metrics['predictions']
            y_true = self.y_test
            
            # Calculate other metrics
            cm = confusion_matrix(y_true, y_pred)
            tn, fp, fn, tp = cm.ravel()
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            comparison.append({
                'Model': name,
                'Accuracy': metrics['accuracy'],
                'AUC-ROC': metrics['auc_roc'],
                'Precision': precision,
                'Recall': recall,
                'F1-Score': f1
            })
        
        results_df = pd.DataFrame(comparison)
        results_df = results_df.sort_values('F1-Score', ascending=False)
        
        print(results_df.to_string(index=False, float_format='%.3f'))
        
        return results_df
    
    def predict_finalists(self):
        """Predict finalists using all data"""
        print("\n PREDICTING FINALISTS")
        print("=" * 50)
        
        # Use the best model based on F1-score
        best_model_name = max(self.results.items(), key=lambda x: x[1]['f1'])[0] if 'f1' in self.results[list(self.results.keys())[0]] else \
                         max(self.results.items(), key=lambda x: x[1]['accuracy'])[0]
        best_model = self.models[best_model_name]
        
        print(f"Using best model: {best_model_name}")
        
        
        # Prepare all data for prediction
        feature_columns = self.X.columns.tolist()
        X_all = self.df[feature_columns].dropna()
        
        # Get corresponding team names
        team_indices = X_all.index
        teams = self.df.loc[team_indices, 'Squad']
        
        # Scale if using scaled model
        if best_model_name == 'Logistic Regression':
            X_all_scaled = self.scaler.transform(X_all)
            probabilities = best_model.predict_proba(X_all_scaled)[:, 1]
        else:
            probabilities = best_model.predict_proba(X_all)[:, 1]
        
        # Create results dataframe
        results = pd.DataFrame({
            'Team': teams,
            'Finalist_Probability': probabilities
        })
        
        # Sort by probability
        results = results.sort_values('Finalist_Probability', ascending=False)
        
        
        # Show predicted finalist pairs
        print("\n PREDICTED FINALIST PAIRS:")
        top_2 = results.head(2)
        for idx, row in top_2.iterrows():
            print(f" {row['Team']} ({row['Finalist_Probability']:.3%})")
        
        return results
    

# Main execution
def main():
    """Main function to run the prediction"""
    
    # Initialize predictor
    predictor = WorldCupFinalistPredictor('aggregated_team_stats_with_appearances.xlsx')
    
    # Prepare data and build models
    predictor.prepare_data()
    predictor.build_models()
    
    # Evaluate models
    results = predictor.evaluate_models()
    
    # Predict finalists
    final_predictions = predictor.predict_finalists()
    
    return predictor, final_predictions

if __name__ == "__main__":
    predictor, predictions = main()

