import torch.nn.functional as F

# efficent gradient clear (better than optim.zero_grad)
def flushGrads(model):    
    for param in model.parameters():
        param.grad = None 
    
# single optimization iteration
def train(model, criterion, optimizer, scheduler, loader, device):
    
    batch_total = 0.0
    accuracy = 0.0
    average_loss = 0.0
    labels = []
    predictions = []
    
    model.train()
    for idx, (inputs, targets) in enumerate(loader):
        inputs, targets = inputs.to(device), targets.to(device)
        flushGrads(model)
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        average_loss += loss
        preds = F.softmax(outputs, dim=1).argmax(dim=1)
        batch_total += 1
        labels.extend(targets.detach().cpu().numpy())
        predictions.extend(preds.detach().cpu().numpy())

    average_loss /=  batch_total
    average_loss = average_loss.detach().cpu().numpy()

    return (predictions, labels, average_loss)

# single validation iteration
def evaluate(model, criterion, optimizer, scheduler, loader, device):

    batch_total = 0.0
    accuracy = 0.0
    average_loss = 0.0
    labels = []
    predictions = [] 
    
    model.eval()
    with torch.no_grad():
        for idx, (inputs, targets) in enumerate(loader):
            inputs, targets = inputs.to(device), targets.to(device)
            flushGrads(model)
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            average_loss += loss
            preds = F.softmax(outputs, dim=1).argmax(dim=1)
            batch_total += 1
            labels.extend(targets.detach().cpu().numpy())
            predictions.extend(preds.detach().cpu().numpy())

    average_loss /=  batch_total
    average_loss = average_loss.detach().cpu().numpy()
    
    return (predictions, labels, average_loss)