#include <bits/stdc++.h>
#include <cmath>

using namespace std;

struct node
{
    int val;
    struct node* left;
    struct node* right;
    int ht;
    
    node(int x)
    {
        left=NULL;
        right=NULL;
        val=x;
        ht=0;
    }
};

int max(int a,int b)
{
    if(a>b)return a;
    else return b;
}

int height( node* T)
{
    if(T==NULL)return -1;
    else return T->ht;
}

node* LeftRotate(node *root)
{
    node* nroot = root->right;
    node * t2 = root->right->left;
    nroot->left=root;
    nroot->left->right=t2;
    root->ht = max(height(root->left), height(root->right))+1; 
    nroot->ht = max(height(nroot->left), height(nroot->right))+1;
    cout<<"gone"<<endl;
    return nroot; 
}

node* RightRotate(node *root)
{
    node* nroot = root->left;
    node * t2 = root->left->right;
    nroot->right=root;
    nroot->right->left =t2;
    root->ht = max(height(root->left), height(root->right))+1; 
    nroot->ht = max(height(nroot->left), height(nroot->right))+1; 
  
    return nroot; 
}


node * insert(node * root,int val)
{
	if(root== NULL)
    {
        root = new node(val);
        return root;
    }
    else if(val < root->val)
    {
        root->left= insert(root->left, val);
    }
    else if(val > root->val)
    {
        root->right= insert(root->right, val);
    }
    
    root->ht = 1+ max(height(root->left),height(root->right));
    
    int bf= height(root->left)-height(root->right);
    
    if(bf > 1 && root->left->right==NULL)
    {
        root=RightRotate(root);
    }
    else if(bf > 1 && root->left->left==NULL)
    {
        root->left=LeftRotate(root->left);
        root=RightRotate(root);
    }
    else if(bf < -1 && root->right->left==NULL)
    {
        cout<<"its"<<endl;
        root=LeftRotate(root);
    }
    else if(bf< -1 && root->right->right==NULL)
    {
         root->right=RightRotate(root->right);
         root=LeftRotate(root);
    }
    return root;
}

void preOrder(struct node *root) 
{ 
    if(root != NULL) 
    { 
        cout<<root->val<<" "; 
        preOrder(root->left); 
        preOrder(root->right); 
    }

} 
  
/* Drier program to test above function*/
int main() 
{ 
  struct node *root = NULL; 
  
  /* Constructing tree given in the above figure */
  root = insert(root, 10); 
  cout<<"done"<<endl;
  root = insert(root, 20);
  cout<<"done"<<endl;
  root = insert(root, 30); 
  cout<<"done"<<endl;
  root = insert(root, 40); 
  root = insert(root, 50); 
  root = insert(root, 25); 
  
  /* The constructed AVL Tree would be 
            30 
           /  \ 
         20   40 
        /  \     \ 
       10  25    50 
  */
  
  printf("Preorder traversal of the constructed AVL"
         " tree is \n"); 
  preOrder(root); 
  cout<<endl;
  
  return 0; 
} 